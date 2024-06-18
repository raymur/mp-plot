TODOS
probably a good idea to sort the todos based on priority for MVP

MVP
 - improve date x axis labeling (done)
 - provide key for colors (done)
 - update pandas/plot logic in the api (DONE)
 - filter out ice leads (done)
 - UI improvements
     - use attractive components & MP theme colors (done)
     - widen search field (done)
     - change text on search button (done)
     - loading icons while waiting for response (done)
     - front end dont submit bad url (done)
 - use different file for csvs, dfs, and plots in a data dir (& fix bug of past ticks not getting refreshed) (done)
 - bug: make sure color map works when only 2 disaplines (ie sport/trad) (done)
 - bug: edgecase null values sport/trad route type (done)
 - handling error, axios vs fetch, how to send error from flask (done)
 - get running in production
    - get flask/cors prod ready (done)
    - decide where to host/deploy (heroku app!!!! basic/eco) (done)
    - is it an issue to store files in data dir??  (dont think so, might crash and have to be restarted though)
    - resolve size of application, reduce node and python modules (node solved, python data science libs are bigggg)
    - get backend to be hit (done)
    - configure (done)


Subsequent Improvemnts
 - minimize directory by cleaning up notebook files (done)
 - better title naming convention for plot (ie 'ray-murphy' -> "Ray Murphy\'s ticks") (done)
 - form for more custom graph options (groom more)
 - local storage for last used url
 - analystics for how many submitted queries
 - smooth transitions for displaying / changing plot
 - github workflows + dev branch
 - caching tick df's in files for multiple runs and graph generations
 - best fit line?
 - improve letter grade normalized rating codes
 - ability to upload excel file for private ticks
 - constraints for generating graph
 - add bouldering and ice 
 - advertise on MP forums & reddit
