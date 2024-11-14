var knex = require('knex')({
    client: 'mysql2',
    connection: {
        host : 'localhost',
        user : 'root',
        password : '12345678',
        database : 'tripwise'
     }
});

module.exports = knex