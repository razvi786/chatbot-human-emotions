class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key == "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }
  toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    var happy = document.getElementById("happy");
    var sad = document.getElementById("sad");
    var neutral = document.getElementById("neutral");
    // var percentage = document.getElementById("percentage");
    var emotions = document.getElementById("emotions");

    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    // 'http:// 127.0.0.1:5000/predict
    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = "";
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
      });

    fetch($SCRIPT_ROOT + "/mood", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((mood) => {
        // alert("hello: " + r);
        console.log("Mood: ", mood);
        // console.log
        // happy.style.display = "block";
        // happy.innerHTML = "";
        if (mood.answer === "happy") {
          console.log("happy---");
          happy.style.display = "block";
          sad.style.display = "none";
          neutral.style.display = "none";
        } else if (mood.answer === "sad") {
          console.log("sad---");
          happy.style.display = "none";
          sad.style.display = "block";
          neutral.style.display = "none";
        } else {
          console.log("neutral---");
          happy.style.display = "none";
          sad.style.display = "none";
          neutral.style.display = "block";
        }
        // percentage.innerText = mood.percentage + "% " + mood.answer;
        // percentage.style.display = "block";
        if (mood.emotions.length > 0) {
          console.log("Emotions list is not empty");
          emotions.innerText = "Emotions: " + mood.emotions;
          emotions.style.display = "block";
        } else {
          console.log("Emotions list is empty");
          emotions.style.display = "none";
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name === "Sam") {
          html +=
            '<div class="messages__item messages__item--visitors">' +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
