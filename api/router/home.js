const Router2 = require("express").Router()

Router2.get("/",  (req , res) => {
    res.send("home")
})



module.exports = Router2

// CRUD : ==> create / read / update / delete