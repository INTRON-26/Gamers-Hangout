const express = require('express');
const UserModel = require('../models/UserModel');
const router = express.Router();

router.post('/register', async (req, res) => {
    const {username,email, password} = req.body;

    const user = new UserModel(username, email, password);

    try{
        const SavedUser = await user.save();
        res.send(SavedUser);
    } catch(err) {
        res.status(404).send(err);
    }
})

module.exports = router;