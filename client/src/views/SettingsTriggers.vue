<template>
  <h5 class="uk-margin-remove-top uk-text-bold uk-margin-small-bottom">
    Triggers
  </h5>
  <div class="uk-form-horizontal uk-margin-large">
    <div class="uk-margin">
      <label class="uk-form-label" for="idle-time-input">Idle Time for Serial Reading</label>
      <div class="uk-form-controls">
        <input class="uk-input" id="idle-time-input" type="number" placeholder="Idle time in seconds"
          v-model="idleTime">
      </div>
    </div>
  </div>
  <div class="uk-form-horizontal uk-margin-large">
    <div class="uk-margin">
      <label class="uk-form-label" for="trigger-time-input">Time to wait before triggering:</label>
      <div class="uk-form-controls">
        <input class="uk-input" id="trigger-time-input" type="number" placeholder="Trigger time in seconds"
          v-model="triggerTime">
      </div>
    </div>
  </div>
  <div class="uk-form-horizontal uk-margin-large" v-for="(input, index) in triggerInputs" :key="index"
    ref="triggerInputs">

    <div class="uk-margin">
      <h6 class="uk-heading-line uk-text-right"><span>Trigger Element {{ index }}</span></h6>
      <label class="uk-form-label" :for="`trigger-value-input-${index}`">Trigger Value</label>
      <div class="uk-form-controls">
        <input class="uk-input" :id="`trigger-value-input-${index}`" type="text" v-model="input.value">
      </div>
    </div>
    <div class="uk-margin">
      <label class="uk-form-label" :for="`trigger-device-input-${index}`">Trigger Device</label>
      <div class="uk-form-controls">
        <input class="uk-input" :id="`trigger-device-input-${index}`" type="text" v-model="input.device">
      </div>
    </div>
    <a class="uk-button uk-button-default" @click="removeTrigger(index)">Remove {{ index }}</a>
  </div>
  <hr />
  <div class="uk-button-group">
    <a class="uk-button uk-button-primary" @click="addTrigger">Add Trigger</a>
    <a class="uk-button uk-button-secondary" @click="saveTriggers">Save Triggers</a>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Settings - Triggers",
  components: {},
  data() {
    return {
      triggerInputs: [],
      idleTime: 0,
      triggerTime: 0,
    }
  },
  setup() {
  },
  mounted() {
    axios
      .get("/interact_triggers")
      .then((response) => {
        // handle success
        if (response.status == 200) {
          console.log(response.data);
          this.triggerInputs = response.data.triggers;
          this.idleTime = response.data.idleTime;
          this.triggerTime = response.data.triggerTime;
        }
      })
      .catch((error) => {
        console.error(error);
      })
      .then(() => { });
  },
  methods: {
    addTrigger() {
      this.triggerInputs.push({ value: '', device: '' });
    },
    removeTrigger(index) {
      this.triggerInputs.splice(index, 1);
    },
    saveTriggers() {
      axios.post('/interact_triggers', {
        triggers: this.triggerInputs,
        idleTime: this.idleTime,
        triggerTime: this.triggerTime,
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  },
};
</script>
