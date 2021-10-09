![BirdsEye by Shengchen Zhang and Zixuan Wang](./assets/cover.png)

<h1 align="center">BirdsEye: Reading the Blue Bird using bird's eye view</h1>
<p align="center">A project submitted to the <a href="https://uist.acm.org/uist2021/cfp.html#sic">UIST 2021 Student Innovation Contest.</p>
<p align="center">
  <a href="https://drive.google.com/file/d/1t6ZZkvQ8wNURpF4umpO3X2qT0VfmAlvU/view">Video preview</a> | <a href="https://github.com/shaunabanana/birdseye/issues">Share ideas</a> | <a href="https://github.com/shaunabanana/birdseye-toio">Go to Toio code</a>
</p>

## Concept
![An image showing rotating, reclustering, and linking robot to read Tweets](./assets/concept.png)
BirdsEye helps you break out of the Twitter echo chamber with a multi-robot interface.

**Social media sites are an increasingly popular place for news and public discourse.** However, the current **algorithmic recommendation is creating echo chambers** that limits the users to similar posts they tend to like, which may result in social polarization and extremism.

By utilizing a projector and toio robots, we present a new way of browsing social media content that gives the user **a bird’s eye view of all the different viewpoints** regarding a topic and enables the user to **directly interact with the algorithm**.

The user can **cluster, browse, link, and regroup** social media posts using intuitive interaction with the robots by moving, flipping, joining and tapping the robots. By directly interact with different viewpoints and the clustering algorithm, our application can help the user break out of the echo chamber and gain a comprehensive view on a topic.

To learn more, [read our contest submission](https://shengchen.design/files/birdseye_uist21_sic.pdf)!

## Note on the dataset
This project uses data based on [this public COVID-19 vaccination tweet dataset](https://www.kaggle.com/gpreda/all-covid19-vaccines-tweets), combined with custom scraping code (in `dataset/scrape.py`) to locate tweets with replies and scrape the conversation. The final dataset is deployed in `public/dataset`.

## Project setup
> NOTE: This project requires code from [another repository to control the Toio robots](https://github.com/shaunabanana/birdseye-toio).

### 0. Setup Nginx server to avoid CORS problems
```
# In your nginx.conf
location / {
    proxy_pass http://127.0.0.1:8080;
}

location /cluster/ {
    proxy_pass http://127.0.0.1:5000;
}

location /keyword/ {
    proxy_pass http://127.0.0.1:5000;
}

location /toio {
    rewrite ^/toio(.*) /$1 break;
    proxy_pass http://127.0.0.1:8175;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    proxy_set_header Host $host;
}
```

### 1. Start computing service
```
pip install -r requirement.txt
cd service
python api.py
```

### 2. Run code in birdseye-toio
```
npm install
# Compile latest toio.js and add to node_modules
npm start
# Turn on your robots one by one, and look for confirmation of connection in console
```

### 3. Run birdseye frontend
```
npm install
npm run serve
```

### 4. Initialize system state
Double tap any toio robot upside-down to reset the system state and start playing!
