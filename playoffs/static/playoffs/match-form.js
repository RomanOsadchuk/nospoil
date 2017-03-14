
Vue.component('match-form', {
  props: ['position'],
  template: `
    <div :id="'match-' + position" class="match-form">
      <div class="input-group">
        <input type="text" class="form-control side-a" placeholder="first side"
               v-bind:readonly="isReadonlyA"
               :name="'side-a-' + position" :value="match.sideA" @input="inpA">
        <span class="input-group-btn">
          <button @click="btnA" :class="match.winnerA == 'True' ? 'btn-success' : 'btn-default'"
                  class="btn btn-a" type="button">won</button>
        </span>
      </div>
      <div class="input-group">
        <input type="text" class="form-control side-b" placeholder="second side"
               v-bind:readonly="isReadonlyB"
               :name="'side-b-' + position" :value="match.sideB" @input="inpB">
        <span class="input-group-btn">
          <button @click="btnB" :class="match.winnerA == 'False' ? 'btn-success' : 'btn-default'"
                  class="btn btn-b" type="button">won</button>
        </span>
      </div>
      <input type="text" class="form-control input-sm youtube-id" placeholder="youtube id"
             :name="'youtube-id-' + position" v-model="youtubeId">
      <input type="hidden" class="winner-a" :name="'winner-a-' + position" v-model="match.winnerA">
    </div>
  `,
  data: function () {
    return {
      playoff: playoff,
      match: matches[this.$props.position],
      youtubeId: ''
    }
  },
  computed: {
    isReadonlyA: function() {
      var round = parseInt(this.$props.position.replace('l', '').split('-')[0])
      if (this.$props.position[0] != 'l')
        return this.playoff.rounds > round + 1
      if (round % 2 == 0)
        return false
      return this.playoff.rounds * 2 > round + 3
    },
    isReadonlyB: function() {
      var round = parseInt(this.$props.position.replace('l', '').split('-')[0])
      if (this.$props.position[0] != 'l')
        return this.playoff.rounds > round + 1
      return this.playoff.rounds * 2 > round + 3
    }
  },
  methods: {
    inpA: function(event) {
      this.match.sideA = event.target.value
      if (this.match.winnerA == 'True')
        this.$emit('update')
    },
    inpB: function(event) {
      this.match.sideB = event.target.value
      if (this.match.winnerA == 'False')
        this.$emit('update')
    },
    btnA: function(event) {
      this.match.winnerA = (this.match.winnerA == 'True') ? 'None': 'True'
      event.target.blur()
      this.$emit('update')
    },
    btnB: function(event) {
      this.match.winnerA = (this.match.winnerA == 'False') ? 'None': 'False'
      event.target.blur()
      this.$emit('update')
    }
  }
})
