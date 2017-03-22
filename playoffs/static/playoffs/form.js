

Vue.component('checkbox-switcher', {
  props: ['isTicked', 'tickedBtn', 'untickedBtn', 'tickedPh', 'untickedPh'],
  template: `
    <div class="input-group">
      <span class="input-group-btn">
        <button type="button" class="btn" @click="emitSignal('untick', $event)"
                :class="isTicked ? 'btn-default' : 'btn-success'">{{ untickedBtn }}</button>
      </span>
      <input type="text" class="form-control text-center"
             :placeholder="isTicked ? tickedPh : untickedPh" readonly>
      <span class="input-group-btn">
        <button type="button" class="btn" @click="emitSignal('tick', $event)"
                :class="isTicked ? 'btn-success' : 'btn-default'">{{ tickedBtn }}</button>
      </span>
    </div>
  `,
  methods: {
    emitSignal: function(signal, event) {
      event.target.blur()
      this.$emit(signal)
    }
  }
})


Vue.component('match-form', {
  props: ['match'],
  template: `
    <div class="match-form">
      <div class="input-group">
        <input type="text" class="form-control side-a" placeholder="first side"
               :value="match.side_a" @input="setSide('side_a', $event)">
        <span class="input-group-btn">
          <button type="button" class="btn btn-a" @click="setWinnerA(true, $event)"
                  :class="match.winner_a===true ? 'btn-success' : 'btn-default'">won</button>
        </span>
      </div>
      <div class="input-group">
        <input type="text" class="form-control side-b" placeholder="second side"
               :value="match.side_b" @input="setSide('side_b', $event)">
        <span class="input-group-btn">
          <button class="btn btn-b" type="button" @click="setWinnerA(false, $event)"
                  :class="match.winner_a===false ? 'btn-success' : 'btn-default'">won</button>
        </span>
      </div>
      <input type="text" class="form-control input-sm youtube-id" placeholder="youtube url or id"
             :value="match.youtube_id" @change="setYoutubeId">
    </div>
  `,
  methods: {
    setSide: function(side, event) {
      this.$emit('update', this.match.position, side, event.target.value)
    },
    setWinnerA: function(val, event) {
      event.target.blur()
      var value = (this.match.winner_a === val) ? null: val
      this.$emit('update', this.match.position, 'winner_a', value)
    },
    setYoutubeId: function(event) {  
      var value = event.target.value
      if (value.includes('?v='))
        value = value.split('?v=')[1].split('&')[0]
      // todo - update with no recursion
      this.$emit('update', this.match.position, 'youtube_id', value)
    }
  }
})



Vue.component('playoff-table', {
  props: ['grid', 'rounds', 'isWinners'],
  template: `
    <div class="playoff-table-outter wrapper flipped">
      <table class="table playoff-table flipped">
        <tbody>
          <tr class="round-names">
            <template v-for="(rnd, index) in grid" v-if="hidden <= index">
              <th v-if="shrinked <= index" style="min-width: 220px">{{ longName(index) }}</th>
              <th v-else>{{ index - hidden + 1 }}</th>
            </template>
          </tr>
          <tr v-if="!isNotShrinkable(0)" class="actions">
            <template v-for="(rnd, index) in grid" v-if="hidden <= index">
              <td v-if="isNotShrinkable(index)">..</td>
              <td v-else-if="shrinked <= index">
                <a href="#" @click.prevent="shrinked = index + 1">&gt collapse &lt</a>
              </td>
              <td v-else><a href="#" @click.prevent="shrinked = index">&lt&gt</a></td>
            </template>
          </tr>
          <tr class="matches">
            <template v-for="(rnd, index) in grid" v-if="hidden <= index">
              <td v-if="shrinked <= index" :class="spacing(index)">
                <match-form v-for="match in rnd" :match="match" :key="match.position"
                            @update="updateGrid"></match-form>
              </td>
              <td v-else></td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data: function() {
    return {shrinked: 0, hidden: 0}
  },
  watch: {
    rounds: function() {
      var total = this.grid.length, rounds = this.rounds
      this.hidden = this.isWinners ? total-rounds : total-rounds*2+2
    }
  },
  methods: {
    longName: function(index) {
      var idxFromEnd = this.grid.length - 1 - index
      if (this.isWinners && idxFromEnd < 3)
        return ['Final', 'SemiFinals', 'QuarterFinals'][idxFromEnd]
      if (idxFromEnd == 0)
        return 'Final'
      return 'Round ' + (index - this.hidden + 1)
    },
    isNotShrinkable: function(index) {
      var idxFromEnd = this.grid.length - 1 - index
      return this.isWinners ? idxFromEnd < 3 : idxFromEnd < 4
    },
    spacing: function(index){
      var toSubtr = Math.max(this.shrinked, this.hidden)
      if (this.isWinners)
        return 'spacing-' + (index - toSubtr + 1)
      return 'spacing-' + (parseInt(index/2) - parseInt(toSubtr/2) + 1)
    },
    updateGrid: function(position, key, val){
      var len = this.grid.length - 1,
          rnd = len - position.replace('l', '').split('-')[0],
          idx = position.split('-')[1] - 1
      this.$emit('update', rnd, idx, key, val)
    }
  }
})


var playoffForm = new Vue({
  el: '#playoff-form',
  delimiters: ['${','}'],
  data: {
    playoff: {
      title: '', sport: '', rounds: 5, double: true,
      private: false, grid: {winners: [], loosers: []}
    },
    roundOptions: [
      { text: '2 rounds', value: 2 },
      { text: '3 rounds', value: 3 },
      { text: '4 rounds', value: 4 },
      { text: '5 rounds', value: 5 }
    ]
  },
  computed: {
    isCreateForm: function() { 
      return document.location.pathname.includes('new')
    },
    apiUrl: function() {
      return document.location.origin + '/api/'
    },
    showLoosersGrid: function() {
      return this.isCreateForm ? this.playoff.double : this.playoff.grid.loosers
    }
  },
  created: function () {
    var vm = this, pk = document.location.pathname.split('/')[3]
    if (this.isCreateForm)
      $.get(vm.apiUrl + 'empty-grid/',
            function(data) { vm.playoff.grid = data })
    else
      $.get(vm.apiUrl + 'playoff/' + pk + '/',
            function(data) { vm.playoff = data })
  },

  methods: {
    setSingleElimination: function() {
      this.playoff.double = false
      $('a[href="#winners"]').tab('show')
    },
    updateWinners: function(rnd, idx, key, val) {
      this.playoff.grid.winners[rnd][idx][key] = val
      var winner = this.getMatchWinner('winners', rnd, idx),
          nextKey = idx % 2 ? 'side_b' : 'side_a'
      if (rnd < this.playoff.grid.winners.length - 1)
        this.updateWinners(rnd+1, parseInt(idx/2), nextKey, winner)
      else if (this.playoff.grid.loosers) {
        var looser = this.getMatchLooser('winners', rnd, idx),
            lasRnd = this.playoff.grid.loosers.length - 1
        this.playoff.grid.final['side_a'] = winner
        this.playoff.grid.loosers[lasRnd][0]['side_a'] = looser
      }
    },
    updateLoosers: function(rnd, idx, key, val) {
      this.playoff.grid.loosers[rnd][idx][key] = val
      var winner = this.getMatchWinner('loosers', rnd, idx),
          nextKey = (rnd%2 && idx%2==0) ? 'side_a' : 'side_b',
          nextIdx = rnd % 2 ? parseInt(idx/2) : idx
      if (rnd < this.playoff.grid.loosers.length - 1)
        this.updateLoosers(rnd+1, nextIdx, nextKey, winner)
      else
        this.playoff.grid.final['side_b'] = winner
    },
    updateFinal: function(position, key, val){
      this.playoff.grid.final[key] = val
    },
    getMatchWinner: function(grd, rnd, idx) {
      if (this.playoff.grid[grd][rnd][idx]['winner_a'] === true)
        return this.playoff.grid[grd][rnd][idx]['side_a']
      if (this.playoff.grid[grd][rnd][idx]['winner_a'] === false)
        return this.playoff.grid[grd][rnd][idx]['side_b']
      return ''
    },
    getMatchLooser: function(grd, rnd, idx) {
      if (this.playoff.grid[grd][rnd][idx]['winner_a'] === true)
        return this.playoff.grid[grd][rnd][idx]['side_b']
      if (this.playoff.grid[grd][rnd][idx]['winner_a'] === false)
        return this.playoff.grid[grd][rnd][idx]['side_a']
      return ''
    },

    collectData: function() {
      var data = {title: this.playoff.title,
                  sport: this.playoff.sport,
                  matches: {}}
      if (this.isCreateForm) {
        data.rounds = this.playoff.rounds
        data.double = this.playoff.double
      }
      for (let round of this.playoff.grid.winners)
        for (let match of round)
          data.matches[match.position] = match
      if (this.playoff.grid.loosers) {
        data.matches['0-0'] = this.playoff.grid.final
        for (let round of this.playoff.grid.loosers)
          for (let match of round)
            data.matches[match.position] = match
      }
      return data
    },
    postData: function() {
      var vm = this, data = this.collectData(),
          successUrl = document.location.origin + '/playoffs/',
          ajax_data = {
            type: this.isCreateForm ? 'POST' : 'PUT',
            url: this.apiUrl+'playoff/'+ (this.isCreateForm ? '' : this.playoff.id+'/'),
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function(resp) {
              document.location.href = successUrl + resp.id + '/'
            }   
          }
      if (document.cookie.includes('csrftoken='))
        ajax_data.headers = {
          'X-CSRFTOKEN': document.cookie.split('csrftoken=')[1].split(' ')[0]
        }
      $.ajax(ajax_data)
    }
  }
})
