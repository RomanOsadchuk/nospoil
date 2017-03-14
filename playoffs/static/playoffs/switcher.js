
Vue.component('checkbox-switcher', {
  props: ['inputId', 'inputName', 'isTicked', 'tickedBtn', 'untickedBtn', 'tickedPh', 'untickedPh'],
  template: `
    <div>
      <input v-model="ticked" :id="inputId" :name="inputName" type="checkbox" class="hidden">
      <div class="input-group">
        <span class="input-group-btn">
          <button v-on:click="doUntick" :class="ticked ? 'btn-default' : 'btn-success'"
                  class="btn" type="button">{{ untickedBtn }}</button>
        </span>
        <input type="text" class="form-control text-center" :placeholder="ticked ? tickedPh : untickedPh" readonly>
        <span class="input-group-btn">
          <button v-on:click="doTick" :class="ticked ? 'btn-success' : 'btn-default'"
                  class="btn" type="button">{{ tickedBtn }}</button>
        </span>
      </div>
    </div>
  `,
  data: function () {
    return {ticked: Boolean(this.$props.isTicked)}
  },
  methods: {
    doTick: function(event) {
      this.ticked = true
      event.target.blur()
      this.$emit('ticked')
    },
    doUntick: function(event) {
      this.ticked = false
      event.target.blur()
      this.$emit('unticked')
    }
  }
})
