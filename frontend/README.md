# frontend

## 1. Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## 2. element-ui

```shell
$ npm i element-ui -S
```

Fully import in `main.js`:

```javascript
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';

Vue.use(ElementUI);

new Vue({
  el: '#app',
  render: h => h(App)
});
```

## 3. axios

Install the `axios` package:

```shell
$ npm install axios --save
```

Adds the utility file `http-common.js`:

```javascript
import axios from 'axios'

export const AXIOS = axios.create({
  baseURL: `/api`
})
```

## 4. Disable source maps for production

In `./vue.config.js`, set `productionSourceMap` to false:

```javascript
module.exports = {
  productionSourceMap: false
}
```

## 5. Disable the error unexpected console statement for production build

[reference](https://stackoverflow.com/a/34215651/6086852)
