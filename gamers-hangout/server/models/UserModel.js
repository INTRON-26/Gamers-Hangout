const mongoose = require('mongoose')

const userSchema = new mongoose.Schema({
    username: {
        required: true,
        type: String,
    },
    password: {
        type: String,
        required: true,
        length: 10,
    },
    email : {
        type: String,
        required: true,
        unique: true,
    },
})

module.exports = mongoose.model('User', userSchema)