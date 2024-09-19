const Router2 = require("express").Router()
const ctrl = require("../controller/user")
Router2.get("/", ctrl.get_victims)

module.exports = Router2
