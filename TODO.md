# zetamatrix

`django`, `js`, `postgres`

### To do before deployment (urgent)

1. refine profile section to show all of your games 
2. fix scaling of zm's 
3. make the video 'PLAY ZETAMATRIX' with black background thumbnail and then the heatmap array






- [ ] join zetamatrix (the video)
- [ ] add the log and total contributions to all 4 zetamatrices 
- [ ] See whether it works. 

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

- [ ] Need a playerstats table

- ♕: has held world record
    - Has been top of day 7 leaderboard
- ⚔︎: has come top 10 in daily challenge
    - Not sure currently how to implement
- ♝: have completed 1000 games
    - Can be rendered from user stats
- ♟: have completed 100 games
    - 
- ⚑: have contributed 10,000
    - 

- [ ] ui: Bare bones CSS, maybe some shadows - clean it up. 
- [ ] The 'game' itself is just how many mental arithmetic questions you can solve in 120 seconds (e.g. 5*12, 7+3). 
- [ ] Every time a user plays a 'game' their score is saved. Every user should be able to see their running average score. 
- [ ] in each game, the time taken to solve every single problem (X + Y) needs to be stored in milliseconds and added to a huge database, because I am trying to gather everyone's data in order to figure out which mental arithmetic question is the hardest (e.g. 82*73). 
- [ ] There is a global leaderboard, which is just the top 20 users with the highest running average
- [ ] There is also a daily 'zetamac'. Instead of randomly generating the questions, everyone has 1 chance to do the same 120 second set of questions, which are generated at the start of the day. 
- [ ] Make font CMU serif
- [ ] Add the zetamatrix to the front page?
- [ ] Record 'got wrong' as a flag

# potential website layout: 
- home page (start game, see profile, see zetamatrix)
- zetamatrix (start game, back to home, top contributors)
- profile (games played, average time (all time), )
- game (centered, easy)


- Watch 'contribute to the Zetamatrix' 
    - Miniscule 'company name' 
    - [ ] Go crazy: https://terminalcss.xyz/#DocVariables
