
var spoiled = {winners: 1, loosers: 0}

Vue.component('match-detail', {
  props: ['sideA', 'sideB', 'youtubeSrc', 'round', 'spoiled'],
  template: `
    <div class="match-detail">
      <ul v-if="toSpoil" class="list-group">
        <li class="list-group-item">{{ sideA }}</li>
        <li class="list-group-item">{{ sideB }}</li>
        <button type="button" class="list-group-item watch">watch</button>
      </ul>
      <ul v-else class="list-group">
        <button type="button" class="list-group-item show-one"
                v-on:click="hidden = false">show</button>
      </ul>
    </div>
  `,
  data: function () {
    return { hidden: true }
  },
  computed: {
    toSpoil: function() {
      console.log(this.$props.spoiled, this.$props.round)
      if (this.$props.spoiled >= parseInt(this.$props.round))
        return true
      return !this.hidden
    }
  }
})

new Vue({
  el: '#winners',
  delimiters: ['${','}'],
  data: {
    shrinked: 0,
    hidden: -1,
    spoiled: 1,
    spclasses: ['spacing-1', 'spacing-2', 'spacing-3', 'spacing-4', 'spacing-5']
  },
  watch: {
    shrinked: function (newShrinked) {
      this.updateSpacing()
    }
  },
  methods: {
    updateSpacing: function () {
      for (var i=0; this.shrinked+i<5; i++) {
        this.spclasses[this.shrinked+i] = 'spacing-' + (i+1)
      }
    }
  }
})

new Vue({
  el: '#loosers',
  delimiters: ['${','}'],
  data: {
    shrinked: 0,
    hidden: -1,
    spoiled: 0,
    spclasses: ['spacing-1', 'spacing-1', 'spacing-2', 'spacing-2',
                'spacing-3', 'spacing-3', 'spacing-4', 'spacing-4']
  },
  watch: {
    shrinked: function (newShrinked) {
      this.updateSpacing()
    }
  },
  methods: {
    updateSpacing: function () {
      for (var i=0, j=1; this.shrinked+i<8; i++) {
        this.spclasses[this.shrinked+i] = 'spacing-' + j
        j = (this.shrinked+i) % 2 == 0 ? j : j+1
      }
    }
  }
})
