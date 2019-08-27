# simple-twitter
A simple Twitter using Flask and Redis

About Redis configuration:
- To avoid data loss completely when the power is corrupted or issue with the physical server, Redis is using an AOF persistence logs every write operation received by the server.


Tutorial:
- This example is using python 3.6 as a primarily programming language with the powerful support of Flask, Redis as a in-memory database
- Redis is run as a container with file `docker-compose.yaml` can be found in `deploy` folder
- API Swagger link: `http://127.0.0.1:$HostPort/api/v1/`

Model:
- The model `Tweet` in `models/` was designed as a circular linked list which chained to a `Tweet` that was retweeted.
- The whole model is designed with json format as followed:
```
{
    "user_name": self.user_name,
    "title": self.title,
    "body": self.body,
    "retweet": self.retweet,
    "count_retweet": self.count_retweet,
    "id": self.id,
    "created_at": self.created_at
}
```

Demo:
- To fake data: Go to the Swagger route and call the `POST /tweet` API with the input as followed:
```angular2
{
  "user_name": "baonq",
  "title": "What a day",
  "body": "All the contents go here",
  "count_retweet": 0
}
```
- `count_retweet` would be default as 0, but we can set it manually for testing the sort process
- To retweet: call the `POST /retweet` API with the input as followed:
```angular2
{
  "user_name": "baonq",
  "title": "What a day",
  "body": "All the contents go here",
  "retweet": "###With an ID goes here",
  "count_retweet": 0
}
```
- Field `retweet` is an `id` of Tweet which can be found in response of `POST /tweet`
- The code will loop all the elements in linked list and increase the `count_retweet` by 1 for every `Tweet` in that list which can be found in `models/Tweet.increase_counter()`

- See all top 10 tweets with order in link: http://127.0.0.1:5000/


To scale up:
- Although there are a lot of methodology to scale up the server when data are getting bigger than the available memory, I think this could work around with 2 ways:
    - Partitioning: It allows for much larger databases, using the sum of the memory of many computers. And easily to scale the physical memory up.
    - Using as virtual memory: Redis will store some indexes which can be a part of total data. Total data will be stored on disk. In this example, I think I would store the `id` and `count_retweet` on redis for optimizing the retweeting and sorting process.