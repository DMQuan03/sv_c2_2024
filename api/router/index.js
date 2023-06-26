const HomeRoute = require("./home")
const User = require("./user")
const Router = (app) => {
    app.use("/" , HomeRoute)
    app.use("/api/user" , User)
}

module.exports = Router