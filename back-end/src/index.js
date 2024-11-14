const express = require('express')
const cors = require('cors')

const routes = require('./routes/routes')

const app = express()
app.use(cors())
app.use(express.json())
app.use(routes);

app.listen(4000, ()=>{
    console.log("Servidor rodando em http://localhost:4000")
})

app.get('/',(request,response)=>{
    response.send("Hello world")
 })