
playoff = {};


// ==== scripts for display view ==== //

playoff.gridViewing = {
  init: function() {
    this.initYoutubeWatching();
    this.initMatchShowing();
  },

  initYoutubeWatching: function() {
    $('.watch-yt').click(function(){
      var side1 = $(this).closest('ul').find('li:eq(0)').text(),
          side2 = $(this).closest('ul').find('li:eq(1)').text();
      $('#video h3').text(side1 + ' - ' + side2);
      $('#ytplayer').attr('src', $(this).data('youtube-src'));
      $('a[href="#video"]').tab('show');
    });
  },

  initMatchShowing: function() {
    var grView = this;
    $('#winners .show-all:eq(0)').parent().html('...');
    grView.showCol($('#winners'), 1);
    $('.show-one').click(function(){
      $(this).closest('ul').addClass('hidden')
             .next('ul').removeClass('hidden');
    });
  
    $('.show-all').click(function(e) {
      e.preventDefault();
      var showRow = $(this).closest('tr'),
          colIndex = $(this).closest('td').prevAll().length;
      grView.showCol($(this).closest('.playoff-table'), colIndex);
      $(this).parent().html('...');
      if (!showRow.find('.show-all').length) { showRow.remove(); }
      return false;
    });
  },

  showCol: function(table, index) {
    table.find('tr.matches td:eq('+index+') div.match-detail').each(function(){
      $(this).find('ul:eq(0)').addClass('hidden');
      $(this).find('ul:eq(1)').removeClass('hidden');
    });
  }
};


// ==== scripts for shrinking/expanding columns ==== //

playoff.gridShrinking = {
  init: function() {
    this.setShrinkable();
    this.initShrinking();
    this.setSpacing();
  },

  setShrinkable: function() {
    var parent;
    $('#winners .shrink').each(function(){
      parent = $(this).parent();
      if (parent.nextAll().length < 6) parent.html('...');
    });
    $('#loosers .shrink').each(function(){
      parent = $(this).parent();
      if (parent.nextAll().length < 8) parent.html('...');
    });
    if (!$('#winners .shrink').length) { $('#winners .shrink-row').remove(); }
    if (!$('#loosers .shrink').length) { $('#loosers .shrink-row').remove(); }
  },

  initShrinking: function() {
    var grShrink = this;
    $('.shrink').click(function(e) {
      e.preventDefault();
      var i, clicked = $(this).closest('td').prevAll().length,
          rows = $(this).closest('.playoff-table > tbody').children();
      for (i=0; i<clicked; i+=2) {
        rows.find('th:eq('+i+')').removeClass('hidden');
        rows.find('th:eq('+(i+1)+')').addClass('hidden');
        rows.find('td:eq('+i+')').removeClass('hidden');
        rows.find('td:eq('+(i+1)+')').addClass('hidden');
      }
      grShrink.setSpacing();
      return false;
    });

    $('.expand').click(function(e){
      e.preventDefault();
      var i, n = $(this).closest('tr').children().length,
          clicked = $(this).closest('td').prevAll().length,
          rows = $(this).closest('.playoff-table > tbody').children();
      for (i=clicked; i<n; i+=2) {
        rows.find('th:eq('+i+')').addClass('hidden');
        rows.find('th:eq('+(i+1)+')').removeClass('hidden');
        rows.find('td:eq('+i+')').addClass('hidden');
        rows.find('td:eq('+(i+1)+')').removeClass('hidden');
      }
      grShrink.setSpacing();
      return false;
    });
  },

  setSpacing: function() {
    var j = 1, rnd;
    $('#winners .matches td').each(function(){
      rnd = $(this).data('round');
      if (!$(this).hasClass('hidden') && rnd) {
        $(this).removeClass().addClass('spacing-' + j++);
      };
    });
    j = 1;
    $('#loosers .matches td').each(function(){
      rnd = $(this).data('round');
      if (!$(this).hasClass('hidden') && rnd) {      
        $(this).removeClass().addClass('spacing-' + j);
        if (rnd % 2 == 0) j++;
      };
    });
  }
};


// ==== scripts for grid editing (filling match forms) ==== //

playoff.gridEditing = {
  init: function() {
    this.initWinnerChanging();
    this.initSideChanging();
    this.initPrivateSwitching();
    this.initYoutubeIdChanging();
    $('.youtube-id').popover({trigger: 'focus', placement: 'bottom'});
    $('.btn').mouseup(function() { this.blur() });
  },

  initYoutubeIdChanging: function() {
    var temp = '';
    $('.youtube-id').change(function(){
      temp = $(this).val();
      if (temp.includes('?v=')) {
        temp = temp.split('?v=')[1].split('&')[0];
        $(this).val(temp);
      } 
    });
  },

  initPrivateSwitching: function() {
    $('#id_private').prop('checked', true);
    $('#private-off').click(function(){
      $('#private-off').removeClass('btn-default').addClass('btn-success');
      $('#private-on').removeClass('btn-success').addClass('btn-default');
      $('#id_private').prop('checked', false);
      $('#private-info').attr('placeholder', 'everyone can edit');
    });
    $('#private-on').click(function(){
      $('#private-on').removeClass('btn-default').addClass('btn-success');
      $('#private-off').removeClass('btn-success').addClass('btn-default');
      $('#id_private').prop('checked', true);
      $('#private-info').attr('placeholder', 'only you can edit');
    });
  },

  initWinnerChanging: function() {
    var grEdit = this;
    $('.btn-a, .btn-b').click(function(){
      var other, winner, match = $(this).closest('.match-form');
      if ($(this).hasClass('btn-default')) {
        $(this).removeClass('btn-default').addClass('btn-success');
        other = $(this).hasClass('btn-a') ? '.btn-b' : '.btn-a'
        match.find(other).removeClass('btn-success').addClass('btn-default');
        winner = $(this).hasClass('btn-a') ? 'True' : 'False';
        match.find('.winner-a').val(winner);
      }
      else {
        $(this).removeClass('btn-success').addClass('btn-default');
        $(this).closest('.match-form').find('.winner-a').val('None');
      }
      grEdit.setWinner(match);
    });
  },

  initSideChanging: function() {
    var grEdit = this;
    $('.side-a, .side-b').keyup(function(){
        match = $(this).closest('.match-form');
        grEdit.setWinner(match);
    });
  },

  setWinner: function(match) {
    var grEdit = this, winner = '';
    if (match.find('.btn-a').hasClass('btn-success')) winner = 'a';
    if (match.find('.btn-b').hasClass('btn-success')) winner = 'b';
    
    var is_lb = match[0].id.split('-')[1][0] == 'l',
        pos = parseInt(match[0].id.split('-')[2]),
        rnd = parseInt(match[0].id.split('-')[1].replace('l', '')),
        side = match.find('.side-' + winner).val() || '',
        next_letter = pos % 2 ? 'a' : 'b',
        next_round = rnd - 1, next_position, next_match;

    if (is_lb && (next_round % 2 == 0)) { 
      next_position = pos; next_letter = 'b'; }
    else { 
      next_position = parseInt((pos + 1) / 2); }
    if (is_lb) next_round = 'l' + next_round;
    if (match[0].id == 'match-0-1') {
      next_round = '0';  next_position = '0'; next_letter = 'a'; }
    if (match[0].id == 'match-l0-1') {
      next_round = '0';  next_position = '0'; next_letter = 'b'; }

    next_match = $('#match-' + next_round + '-' + next_position);
    if (next_match.length) {
      next_match.find('.side-' + next_letter).val(side);
      grEdit.setWinner(next_match);
    }
  }
};


// ==== scripts for rounds number changing, elimination type changing ==== //

playoff.gridChanging = {
  init: function() {
    this.initDoubleChanging();
    this.initRoundChanging();
  },

  initDoubleChanging: function() {
    $('#id_double').prop('checked', true);
    $('#double-off').click(function(){
      $('#double-off').removeClass('btn-default').addClass('btn-success');
      $('#double-on').removeClass('btn-success').addClass('btn-default');
      $('#id_double').prop('checked', false);
      $('a[href="#winners"]').text('Grid').tab('show');
      $('a[href="#loosers"]').addClass('hidden');
      $('a[href="#final"]').addClass('hidden');
    });
    $('#double-on').click(function(){
      $('#double-on').removeClass('btn-default').addClass('btn-success');
      $('#double-off').removeClass('btn-success').addClass('btn-default');
      $('#id_double').prop('checked', true);
      $('a[href="#winners"]').text('Winners Grid');
      $('a[href="#loosers"]').removeClass('hidden');
      $('a[href="#final"]').removeClass('hidden');
    });
  },

  initRoundChanging: function() {
    var grChange = this, roundsNum = $('#id_rounds').val();
    grChange.changeRoundNumber(roundsNum);
    $('#id_rounds').change(function(){
      roundsNum = parseInt($(this).val());
      grChange.changeRoundNumber(roundsNum);
    });
  },

  changeRoundNumber: function(newRoundNumber) {
    var i, j, temp, row, slice_index,
        winners_current = $('#winners tr:eq(0)').children().length,
        loosers_current = $('#loosers tr:eq(0)').children().length,
        winners_hidden = $('#hidden-winners tr:eq(0)').children().length,
        loosers_hidden = $('#hidden-loosers tr:eq(0)').children().length,
        winners_should_be = newRoundNumber * 2,
        loosers_should_be = newRoundNumber * 4 - 4,
        winner_rows = $('#winners .playoff-table > tbody').children(),
        looser_rows = $('#loosers .playoff-table > tbody').children();

    if (winners_should_be < winners_current) {
      $('#winners tr').each(function(index){
        slice_index = winners_current - winners_should_be;
        temp = $(this).children().slice(0, slice_index).detach();
        row = $('#hidden-winners tr:eq('+index+')');
        temp.appendTo(row);
      });
      $('#loosers tr').each(function(index){
        slice_index = loosers_current - loosers_should_be;
        temp = $(this).children().slice(0, slice_index).detach();
        row = $('#hidden-loosers tr:eq('+index+')');
        temp.appendTo(row);
      });
    }

    if (winners_should_be > winners_current) {
      $('#hidden-winners tr').each(function(index){
        slice_index = winners_hidden + winners_current - winners_should_be;
        temp = $(this).children().slice(slice_index).detach();
        row = $('#winners tr:eq('+index+')');
        temp.prependTo(row);
      });
      $('#hidden-loosers tr').each(function(index){
        slice_index = loosers_current + loosers_hidden - loosers_should_be;
        temp = $(this).children().slice(slice_index).detach();
        row = $('#loosers tr:eq('+index+')');
        temp.prependTo(row);
      });
    }

    $('.playoff-table td:even').addClass('hidden');
    $('.playoff-table th:even').addClass('hidden');
    $('.playoff-table td:odd').removeClass('hidden');
    $('.playoff-table th:odd').removeClass('hidden');

    $('#winners .round-names th:even').each(function(index){
      if (!$(this).text().includes('F')) $(this).text(index + 1);
    });
    $('#winners .round-names th:odd').each(function(index){
      if (!$(this).text().includes('F')) $(this).text('Round ' + (index+1));
    });
    $('#loosers .round-names th:even').each(function(index){
      if (!$(this).text().includes('F')) $(this).text(index + 1);
    });
    $('#loosers .round-names th:odd').each(function(index){
      if (!$(this).text().includes('F')) $(this).text('Round ' + (index+1));
    });

    playoff.gridShrinking.setSpacing();
  }
};


// ==== initialization ==== //

$(document).ready(function(){
  playoff.gridViewing.init();
  playoff.gridShrinking.init();
  playoff.gridEditing.init();
  playoff.gridChanging.init();
});
