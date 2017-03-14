
var vueGrid = new Vue({
  el: '#vue-playoff',
  delimiters: ['${','}'],
  data: { playoff: playoff },
  methods: {
    updateRounds: function(event) {
      this.playoff.rounds = parseInt(event.target.value)
      this.$emit('new-rounds')
    },
    makeSingle: function() {
      this.playoff.double = false
      $('a[href="#winners"]').tab('show')
    }
  }
})

new Vue({
  el: '#tablist',
  data: { playoff: playoff }
})

new Vue({
  el: '#winners',
  delimiters: ['${','}'],
  data: {
    playoff: playoff,
    matches: matches,
    shrinked: 0,
    hidden: 0,
    spclasses: ['spacing-1', 'spacing-2', 'spacing-3', 'spacing-4', 'spacing-5']
  },
  mounted: function () {
    var vm = this
    vueGrid.$on('new-rounds', function () {
      vm.hidden = 5 - this.playoff.rounds
      vm.shrinked = vm.hidden
    })
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
    },
    updateGrid: function (position) {
      var nextPos = _getNextWinners(position)
      if (!nextPos)
        return
      var winner = _getWinner(this.matches[position])
      this.matches[nextPos.position][nextPos.side] = winner
      this.updateGrid(nextPos.position)
    }
  }
})

new Vue({
  el: '#loosers',
  delimiters: ['${','}'],
  data: {
    playoff: playoff,
    matches: matches,
    shrinked: 0,
    hidden: 0,
    spclasses: ['spacing-1', 'spacing-1', 'spacing-2', 'spacing-2',
                'spacing-3', 'spacing-3', 'spacing-4', 'spacing-4']
  },
  mounted: function () {
    var vm = this
    vueGrid.$on('new-rounds', function () {
      vm.hidden = 10 - 2*this.playoff.rounds
      vm.shrinked = vm.hidden
    })
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
    },
    updateGrid: function (position) {
      var nextPos = _getNextLoosers(position)
      if (!nextPos)
        return
      var winner = _getWinner(this.matches[position])
      this.matches[nextPos.position][nextPos.side] = winner
      this.updateGrid(nextPos.position)
    }
  }
})
