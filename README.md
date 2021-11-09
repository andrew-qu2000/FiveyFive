# FiveyFive
In-house teambuilding assistant with generation or manual drag-drop
## Our story
Our group of friends loves playing videogames together online. While we typically use the games' matchmaking systems to play against strangers, perhaps the most exciting matches are "in-houses" - custom lobbies where ten of us play against each other for bragging rights. Like a schoolyard playground, we made teams by choosing two captains, who took turns picking their teammates. In practice, this often led to boring, one-sided games.

Our solution was to give everyone a skill rating (like NBA2K), which would allow us to build two teams with a similar rating. A simple algorithm would run through permutations and choose the closest matchups. This worked okay, but ignored the different positions that players could take, like a basketball team with too many Centers.

So, everyone was then given five ratings, one for each position. Now, there were millions of possible matchups, requiring an optimized algorithm to quickly deliver a close matchup. A frontend UI can then be added so that anyone from the lobby can generate the teams.

## Aims
- Implement brute force teambuilding algorithm
- Implement option to lock players into a position and build around them
- Explore alternative or more elegant algorithms to find good matchups in less time
- Build a web based app with UI allowing for quick manual swapping between players, or teambuild with algorithms
- Derive player skill ratings by using uMMR's API, or by using an original formula
- Create login system for users to save their players and other data
- Allow for player creation or upload of data in a .csv
