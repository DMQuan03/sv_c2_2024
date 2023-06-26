const mongoose = require('mongoose'); // Erase if already required

// Declare the Schema of the Mongo model
var Admin_user = new mongoose.Schema({
    account:{
        type:String,
        default : "Admin123"
    },
    pass_word:{
        type:String,
        default : "Admin123"
    },
    name:{
        type : String,
        default : "AdminDeathWeb"
    },
    role: {
        type : String,
        default : "Admin"
    },
    address: {
        type : Sting,
        default : "127.0.0.1",
        required : true,
        unique: true,
    }
});

//Export the model
module.exports = mongoose.model('User', Admin_user);