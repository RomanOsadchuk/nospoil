var playoff = {
  double: true, 
  rounds: 5,
  roundOptions: [
    { text: '2 Rounds', value: 2 },
    { text: '3 Rounds', value: 3 },
    { text: '4 Rounds', value: 4 },
    { text: '5 Rounds', value: 5 }
  ]
}
var matches = {}
for (var i=0; i<4; i++)
  for (var j=1; j<=2**i; j++)
    matches[i+'-'+j] = {sideA: '', sideB: '', winnerA: ''}
for (var j=1; j<10; j++)
  matches[4+'-0'+j] = {sideA: '', sideB: '', winnerA: ''}
for (var j=10; j<17; j++)
  matches[4+'-'+j] = {sideA: '', sideB: '', winnerA: ''}
for (var i=0; i<8; i++)
  for (var j=1; j<=2**parseInt(i/2); j++)
    matches['l'+i+'-'+j] = {sideA: '', sideB: '', winnerA: ''}

function _getNextWinners(position) {
  var nextRnd = parseInt(position.split('-')[0]) - 1,
      pos = parseInt(position.split('-')[1])
  if (nextRnd < 0)
    return null
  var nextPos = parseInt((pos + 1) / 2),
      nextSide = pos % 2 ? 'sideA' : 'sideB'
  return {position: nextRnd+'-'+nextPos, side: nextSide}
}

function _getNextLoosers(position) {
  var nextRnd = parseInt(position.replace('l', '').split('-')[0]) - 1,
      pos = parseInt(position.split('-')[1])
  if (nextRnd < 0)
    return null
  if (nextRnd % 2 == 0)
    return {position: 'l'+nextRnd+'-'+pos, side: 'sideB'}
  var nextPos = parseInt((pos + 1) / 2),
      nextSide = pos % 2 ? 'sideA' : 'sideB'
  return {position: 'l'+nextRnd+'-'+nextPos, side: nextSide}
}

function _getWinner(matchInfo) {
  if (matchInfo.winnerA == 'True')
    return matchInfo.sideA
  if (matchInfo.winnerA == 'False')
    return matchInfo.sideB
  return ''
}
