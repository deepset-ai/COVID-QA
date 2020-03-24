package com.theapache64.cs.servlets

import com.theapache64.cs.core.Scholar
import com.theapache64.cs.core.SecretConstants
import com.theapache64.cs.models.TelegramUpdate
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.TelegramAPI
import javax.servlet.annotation.WebServlet
import javax.servlet.http.HttpServlet
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse

@WebServlet(urlPatterns = ["/get_response"])
class CoronaScholarServlet : HttpServlet() {

    companion object {
        private const val GITHUB_REPO_URL = "https://github.com/deepset-ai/COVID-QA"

        private val INTRO = """
                    🤖 Ask me anything about COVID-19. I provide trustworthy answers via NLP.
                    Meet my makers <a href="$GITHUB_REPO_URL/graphs/contributors">here</a>
                """.trimIndent()


    }


    override fun doPost(req: HttpServletRequest, resp: HttpServletResponse) {

        val request = parseUpdate(req)
        resp.writer.write("ok") // tell telegram that it's being handled to stop receiving duplicate messages.

        Thread {

            val question = request.message.text.trim()

            val msg = if (question == "/start" || question == "/help") {
                INTRO
            } else {

                // Getting answer
                val answer = Scholar.getAnswer(question)

                if (answer != null && answer.answers.isNotEmpty()) {

                    // Building reply message
                    val ans = answer.answers.first()
                    val confidence = (ans.probability * 100).toInt()
                    val emoji = when (confidence) {
                        in 0..30 -> "❤️" // red = average
                        in 31..70 -> "🧡️" // orange = ok
                        else -> "💚" // green = best
                    }
                    val confString = "$emoji Answer Confidence : $confidence%\n\n"
                    confString + ans.answer + "\n\n \uD83C\uDF0E Source : <a href=\"${ans.meta.link}\">${ans.meta.source}</a>"
                } else {
                    // Invalid query
                    "Sorry, I don't know about that"
                }
            }

            // Sending the message
            TelegramAPI.sendHtmlMessage(
                SecretConstants.BOT_TOKEN,
                "${request.message.chat.id}",
                msg,
                request.message.messageId
            )
        }.start()
    }

    private fun parseUpdate(req: HttpServletRequest): TelegramUpdate {
        val jsonString = req.reader.readText()
        return GsonUtil.gson.fromJson(jsonString, TelegramUpdate::class.java)
    }
}