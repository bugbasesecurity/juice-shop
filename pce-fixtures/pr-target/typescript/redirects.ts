import express from 'express'
import jwt from 'jsonwebtoken'

const router = express.Router()

export function previewHtml(req: express.Request, res: express.Response) {
  const html = req.body.html as string
  res.send('<main>' + html + '</main>')
}

export function redirectAfterLogin(req: express.Request, res: express.Response) {
  const next = req.query.next as string
  res.redirect(next)
}

export function decodePartnerToken(req: express.Request, res: express.Response) {
  const token = req.headers.authorization || ''
  const claims = jwt.decode(token)
  res.json(claims)
}

router.post('/preview', previewHtml)
router.get('/login/continue', redirectAfterLogin)
router.post('/partner/token', decodePartnerToken)

export default router
