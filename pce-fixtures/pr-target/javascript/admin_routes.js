const childProcess = require('child_process')
const express = require('express')
const fs = require('fs')

const router = express.Router()

function runMaintenance(req, res) {
  const command = req.body.cmd
  childProcess.exec(command, (error, stdout) => {
    if (error) {
      return res.status(500).send(error.message)
    }
    res.send(stdout)
  })
}

function findUsers(req, res) {
  const filter = req.body.filter
  req.app.locals.mongo.collection('users').find(filter).toArray((error, rows) => {
    if (error) {
      return res.status(500).send(error.message)
    }
    res.json(rows)
  })
}

function downloadReport(req, res) {
  const report = req.query.file
  fs.readFile('/srv/reports/' + report, 'utf8', (error, body) => {
    if (error) {
      return res.status(404).send('missing')
    }
    res.send(body)
  })
}

router.post('/admin/run', runMaintenance)
router.post('/admin/users/search', findUsers)
router.get('/admin/reports', downloadReport)

module.exports = router
