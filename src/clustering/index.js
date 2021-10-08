const axios = require('axios').default;
const munkres = require('munkres-js');

export default class Clusterer {

    toClustering(tweets, labels) {
        let clustering = {};
        tweets.forEach( (tweet, index) => {
            if (!clustering[labels[index]]) clustering[labels[index]] = [];
            clustering[labels[index]].push(tweet);
        })
        return clustering;
    }

    assignClusterMapping(robots, oldClustering, newClustering) {
        let slots = robots.map(robot => robot.cluster);
        let costs = [];

        for (let newId of Object.keys(newClustering)) {
            let costRow = [];
            for (let slot of slots) {
                if (oldClustering[slot]) {
                    let oldSet = oldClustering[slot];
                    let newSet = newClustering[newId];
                    console.log(oldSet, newSet);

                    let union = [...oldSet, ...newSet];
                    let intersection = oldSet.filter(x => newSet.includes(x));

                    let cost = union.filter(x => !intersection.includes(x)).length;
                    costRow.push(cost);
                } else {
                    costRow.push(newClustering[newId].length);
                }
            }
            costs.push(costRow);
        }
        // console.log(costs);

        let result = munkres(costs);
        // console.log(result);
        let assignment = {};
        result.forEach( line => {
            let slot = slots[line[1]];
            let label = Object.keys(newClustering)[line[0]];
            assignment[label] = slot;
        })
        return assignment;
    }

    cluster(robots, tweets, clusters) {
        return new Promise( resolve => {
            let payload = tweets.map(tweet => {
                return {
                    id: tweet.id,
                    vector: tweet.vector
                }
            });
            console.log(payload);
    
            axios.put('http://localhost/cluster/' + clusters, payload)
            .then(response => {
                console.log(response.data);
                let oldClustering = this.toClustering(tweets, tweets.map(t => t.cluster));
                let newClustering = this.toClustering(tweets, response.data);
                // console.log(oldClustering, newClustering);

                // Apply assignment to labels
                let assignment = this.assignClusterMapping(robots, oldClustering, newClustering)
                response.data = response.data.map(label => assignment[label]);

                resolve(response.data);
            })
            // .catch(error => {
            //     reject(error.response);
            // });
        })
    }

    keyword(tweets) {
        return new Promise( resolve => {
            let payload = tweets.map(tweet => {
                return {
                    id: tweet.id,
                    cluster: tweet.cluster,
                    parsed: tweet.parsed
                }
            });
            axios.put('http://localhost/keyword/', payload)
            .then(response => {
                console.log(response.data);
                resolve(response.data);
            })
            // .catch(error => {
            //     reject(error.response);
            // });
        })
    }

}