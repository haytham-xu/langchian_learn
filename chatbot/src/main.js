import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import ViewUIPlus from 'view-ui-plus'

const app = createApp(App)

app.use(router)
app.use(ViewUIPlus)
app.mount('#app')
