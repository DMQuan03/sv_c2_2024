const jwt = require("jsonwebtoken")
const bcrypt = require("bcrypt")
const User = requied("./asd")

const HomeController ={
    register_user : async(req , res) => {
        try {
            const { user , pass } = req.body
            Is_user = User.findOne({username : user})
            if (user) {
                throw new Error("user already exited !!!")
            }
            new_user = new User ({
                username : user,
                password : pass
            })
            new_user.save()

            return res.status(200).json({
                success : True,
                message : "Register user successfully"
            })
        } catch (error) {
            console.log(error)            
        } finally {
            console.log("DONE !!!")
        }
    },
    login_user : async(req , res) => {
        try {
            const { user , pass} = req.body
            const user_check = User.findOne({username : user})
            if (!user_check) {
                return res.status(404).json({
                    success : False,
                    message : "wrong username"
                })
            }
            is_pass = bcrypt.hash(
                pass,
                user_check.password
            )
            if (!is_pass) {
                throw new Error("wrong password")
            }
            if (user_check && is_pass) {
                console.log("create - token")
            }
        } catch (error) {
            console.log(error)
            return 0
        } finally {
            console.log("DONE !!!")
        }
    }
}

module.exports = HomeController