const axios = require('axios').default;

export default class Clusterer {

    cluster(tweets, clusters) {
        return new Promise( (resolve, reject) => {
            let payload = tweets.map(tweet => {
                return {
                    id: tweet.id,
                    vector: tweet.vector
                }
            });
    
            axios.put('http://localhost/cluster/' + clusters, payload)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.response);
            });
        })
    }

}