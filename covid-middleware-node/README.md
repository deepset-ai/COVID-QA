# Covid Middlware


Middleware for the Covid  Projct

## QuickStart

<!-- add docs here for user -->

see [egg docs][egg] for more detail.

### Development

```bash
$ npm i
$ npm run dev
$ open http://localhost:7001/
```

### Deploy

```bash
$ npm start
$ npm stop
```

### npm scripts

- Use `npm run lint` to check code style.
- Use `npm test` to run unit test.
- Use `npm run autod` to auto detect dependencies upgrade, see [autod](https://www.npmjs.com/package/autod) for more detail.
[egg]: https://eggjs.org

# Documentation

https://github.com/eggjs/egg/blob/master/docs/source/en/basics/

# Run using docker

sudo docker build -t 'backend-api' .
sudo docker run -p 7002:7001 backend-api


# deployment

EGG_SERVER_ENV=production npm start

or :

egg-scripts start --port=7001 --title=egg-server-showcase --env=production


# migratons

run

     sequelize db:migrate
