<template>
    <div id="background-div">
        <div id="chat-history">
            <div v-for="message in messages" :key="message.text">
                <div v-if="message.role === 'AI'">
                    <div style="display: flex; justify-content: flex-start;">
                        <!-- <div style="width: 50px; height: 50px; background-color: #000; border-radius: 50%;"></div> -->
                        <Avatar src="https://i.loli.net/2017/08/21/599a521472424.jpg" size="large" />
                        <div style="border-radius: 10px; padding: 5px; margin: 5px;">{{ message.text }}</div>
                    </div>
                </div>
                <div v-else>
                    <div style="display: flex; justify-content: flex-end;">
                        <div style=" border-radius: 10px; padding: 5px; margin: 5px;">{{ message.text }}</div>
                        <Avatar style="background-color: #87d068" icon="ios-person" size="large"/>
                        <!-- <div style="width: 50px; height: 50px; background-color: #000; border-radius: 50%;"></div> -->
                    </div>
                </div>
            </div>
        </div>
        <div class="intput-box">
            <Input class="input" v-model="input"  @keyup.enter="submit" placeholder="Enter something..." />
            <Button class="button" type="success" @click="submit">Submit</Button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      input: '',
      tabId: "",
      messages: [
        { role: 'AI', text: 'How can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
        // { role: 'AI', text: 'Hello, how can I help you?'},
        // { role: 'Human', text: 'I want to buy a car.'},
      ]
    };
  },
//   mounted: {
//   },
  methods: {
    submit() {
      const message = this.input;
      this.input = '';
      this.messages.push({ role: 'Human', text: message });

      axios.post('http://127.0.0.1:5001/message', {
        tabId:this.tabId,
        humanMessage: message
      })
      .then(response => {
        this.messages.push({ role: 'AI', text: response.data['text'] });
        this.tabId = response.data['tabId'];
      });
    }
  }
};
</script>

<style scoped>
div {
    /* border: 1px solid #000; */
}
#background-div {
    width: 40%;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 30%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #f5f5f5;
}

#chat-history {
    width: 100%;
    /* height: 80%; */
    overflow-y: auto;
    /* margin-bottom: 20px; */
    flex-grow: 1;
}

#input-box {
    width: 100%;
    height: 100px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* .message {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 10px;
} */

/* .message.AI {
    justify-content: flex-end;
} */
/* 
.message .text {
    background-color: #f0f0f0;
    color: #333;
    border-radius: 10px;
    padding: 10px;
    margin: 5px;
    max-width: 70%;
    word-wrap: break-word;
} */

/* .message .avatar {
    width: 50px;
    height: 50px;
    background-color: #000;
    border-radius: 50%;
    margin: 5px;
} */

.intput-box {
    display: flex;
    justify-content: space-between;
}

.input {
  flex-grow: 1;
  margin-left: 10px;
  margin-right: 10px;
}

.button {
  width: 100px;
}
</style>
