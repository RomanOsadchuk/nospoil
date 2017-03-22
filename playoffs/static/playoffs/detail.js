

Vue.component('match-detail', {
  props: ['match', 'index', 'spoiledCol'],
  template: `
    <div class="match-detail">
      <ul class="list-group">
        <template v-if="spoiled || spoiledCol > index">
          <li class="list-group-item">{{ match.side_a || '(tbd)' }}</li>
          <li class="list-group-item">{{ match.side_b || '(tbd)' }}</li>
          <button type="button" class="list-group-item watch" @click="watchMatch"
                  :class="match.youtube_id ? '' : 'disabled'">
            {{ match.youtube_id ? 'watch' : '(no video)' }}
          </button>
        </template>
        <button v-else type="button" class="list-group-item show-one"
                @click="spoiled = true">show</button>
      </ul>
    </div>
  `,
  data: function() {
    return {spoiled: false}
  },
  methods: {
    watchMatch() {
      if (this.match.youtube_id)
        this.$emit('watch', this.match)
    }
  }
})


Vue.component('playoff-table', {
  props: ['grid', 'isWinners'],
  template: `
    <div class="playoff-table-outter wrapper flipped">
      <table class="table playoff-table flipped">
        <tbody>
          <tr class="round-names">
            <template v-for="(rnd, index) in grid">
              <th v-if="shrinked <= index" style="min-width: 220px">{{ longName(index) }}</th>
              <th v-else>{{ index + 1 }}</th>
            </template>
          </tr>
          <tr v-if="!isNotShrinkable(0)" class="actions">
            <template v-for="(rnd, index) in grid">
              <td v-if="isNotShrinkable(index)">..</td>
              <td v-else-if="shrinked <= index">
                <a href="#" @click.prevent="shrinked = index + 1">&gt collapse &lt</a>
              </td>
              <td v-else><a href="#" @click.prevent="shrinked = index">&lt&gt</a></td>
            </template>
          </tr>
          <tr v-if="spoiled < grid.length" class="actions">
            <template v-for="(rnd, index) in grid">
              <td v-if="shrinked > index">..</td>
              <td v-else-if="spoiled <= index">
                <a href="#" @click.prevent="spoiled = index + 1">show all</a>
              </td>
              <td v-else>..</td>
            </template>
          </tr>
          <tr class="matches">
            <template v-for="(rnd, index) in grid">
              <td v-if="shrinked <= index" :class="spacing(index)">
                <match-detail v-for="match in rnd" :match="match" :key="match.position"
                              :spoiledCol="spoiled" :index="index" @watch="watch"></match-detail>
              </td>
              <td v-else></td>
            </template>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data: function() {
    return {
      shrinked: 0,
      spoiled: this.$props.isWinners ? 1 : 0,
    }
  },
  methods: {
    longName: function(index) {
      var idxFromEnd = this.grid.length - 1 - index
      if (this.isWinners && idxFromEnd < 3)
        return ['Final', 'SemiFinals', 'QuarterFinals'][idxFromEnd]
      if (idxFromEnd == 0)
        return 'Final'
      return 'Round ' + (index + 1)
    },
    isNotShrinkable: function(index) {
      var idxFromEnd = this.grid.length - 1 - index
      return this.isWinners ? idxFromEnd < 3 : idxFromEnd < 4
    },
    spacing: function(index) {
      if (this.isWinners)
        return 'spacing-' + (index - this.shrinked + 1)
      return 'spacing-' + (parseInt(index/2) - parseInt(this.shrinked/2) + 1)
    },
    watch: function(match) {
      this.$emit('watch', match)
    }
  }
})


var playoffDetail = new Vue({
  el: '#content',
  delimiters: ['${','}'],
  data: {
    playoff: {title: 'Loading ... ', grid: {'winners': []}},
    watchTitle: 'Select match to watch from grid',
    watchSrc: ''
  },
  created: function () {
    var vm = this, pk = document.location.pathname.split('/')[2],
        apiUrl = document.location.origin + '/api/playoff/' + pk + '/'
    $.get(apiUrl, function(data) { vm.playoff = data })
  },
  methods: {
    watch: function(match) {
      var ytDom = 'https://www.youtube.com/embed/'
      this.watchTitle = match.side_a + ' - ' + match.side_b
      this.watchSrc = ytDom + match.youtube_id + '?controls=0'
      $('a[href="#video"]').tab('show')
    }
  }
})
