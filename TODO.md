# zetamatrix

`django`, `js`, `postgres`

- [ ] ER diagram 
- [ ] Your global ranking (F to A) - Every round you complete nudges your average and your ranking is calculated based off of that? 
- [ ] Only one leaderboard 
    - Questions solved 
    - World record
    - Current fast (last 7 days) 

- [ ] Daily ZetaMatrix
- [ ] Need to rework database model to allow users to see their progress as a line chart. 
    - Games played
    - 30 day average
    - Delta from 30 days ago 
    - Fastest question 
    - Scores over all time

- ♕: has held world record (check every submission)
- ⚔︎: has come top 10 in daily challenge
- ♝: have completed 1000 games
- ♟: have completed 100 games
- ⚑: have contributed 10,000

- [ ] ui: Bare bones CSS, maybe some shadows - clean it up. 
- [ ] The 'game' itself is just how many mental arithmetic questions you can solve in 120 seconds (e.g. 5*12, 7+3). 
- [ ] Every time a user plays a 'game' their score is saved. Every user should be able to see their running average score. 
- [ ] in each game, the time taken to solve every single problem (X + Y) needs to be stored in milliseconds and added to a huge database, because I am trying to gather everyone's data in order to figure out which mental arithmetic question is the hardest (e.g. 82*73). 
- [ ] There is a global leaderboard, which is just the top 20 users with the highest running average
- [ ] There is also a daily 'zetamac'. Instead of randomly generating the questions, everyone has 1 chance to do the same 120 second set of questions, which are generated at the start of the day. 
- [ ] Make font CMU serif
- [ ] Add the zetamatrix to the front page?

# potential website layout: 
- home page (start game, see profile, see zetamatrix)
- zetamatrix (start game, back to home, top contributors)
- profile (games played, average time (all time), )
- game (centered, easy)