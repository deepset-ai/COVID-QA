package com.theapache64.cs.servlets

import com.theapache64.cs.core.Scholar
import com.theapache64.cs.core.SecretConstants
import com.theapache64.cs.models.SendMessageRequest
import com.theapache64.cs.models.TelegramCallbackQuery
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

        // Feedback buttons
        private const val FEEDBACK_RELEVANT_TEXT = "✅ Relevant"
        private const val FEEDBACK_FAKE_TEXT = "😤 Fake!"
        private const val FEEDBACK_IRRELEVANT_TEXT = "😒 Irrelevant"
        private const val FEEDBACK_OUTDATED_TEXT = "📆 Outdated"

        private const val FEEDBACK_RELEVANT_KEY = 'r'
        private const val FEEDBACK_FAKE_KEY = 'f'
        private const val FEEDBACK_IRRELEVANT_KEY = 'i'
        private const val FEEDBACK_OUTDATED_KEY = 'o'

        private const val GITHUB_REPO_URL = "https://github.com/deepset-ai/COVID-QA"

        private val INTRO = """
                    🤖 Ask me anything about COVID-19. I provide trustworthy answers via NLP.
                    Meet my makers <a href="$GITHUB_REPO_URL/graphs/contributors">here</a>
                """.trimIndent()


    }

    private var feedbackQuery: TelegramCallbackQuery? = null

    private fun isFeedback(jsonString: String): Boolean {
        this.feedbackQuery = GsonUtil.gson.fromJson(jsonString, TelegramCallbackQuery::class.java)
        return this.feedbackQuery?.callbackQuery != null
    }


    private fun sendTyping(to: String) {
        Thread {
            TelegramAPI.sendChatAction(
                SecretConstants.ACTIVE_BOT_TOKEN,
                to,
                "typing"
            )
        }.start()
    }

    override fun doPost(req: HttpServletRequest, resp: HttpServletResponse) {

        val jsonString = req.reader.readText()
        if (isFeedback(jsonString)) {

            Thread {

                val feedbackData = feedbackQuery!!.callbackQuery.data

                // Sending typing
                sendTyping("${feedbackQuery!!.callbackQuery.from.id}")

                val feedbackChar = feedbackData[0]
                val modelId = feedbackData.substring(1)
                println("Adding feedback")
                Scholar.addFeedback(modelId, feedbackChar)

                Thread {
                    // Sending feedback to cancel progress animation
                    TelegramAPI.answerCallbackQuery(
                        SecretConstants.ACTIVE_BOT_TOKEN,
                        feedbackQuery!!.callbackQuery.id
                    )
                }.start()

                // Sending thanks
                TelegramAPI.sendHtmlMessage(
                    SecretConstants.ACTIVE_BOT_TOKEN,
                    "${feedbackQuery!!.callbackQuery.message.chat.id}",
                    "Thank you for your feedback 🤗",
                    feedbackQuery!!.callbackQuery.message.messageId,
                    null
                )


            }.start()
        } else {
            // Normal response
            handleNormalResponse(jsonString, resp)
        }
    }


    private fun handleNormalResponse(jsonString: String, resp: HttpServletResponse) {
        val request = GsonUtil.gson.fromJson(jsonString, TelegramUpdate::class.java)
        resp.writer.write("ok") // tell telegram that it's being handled to stop receiving duplicate messages.

        Thread {

            sendTyping(request!!.message.from.id.toString())

            val question = request.message.text.trim()

            var modelId: String? = null
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

                    // Setting modelId to get feedback
                    modelId = ans.meta.documentId

                    val confString = "$emoji Answer Confidence : $confidence%\n\n"
                    confString + ans.answer + "\n\n \uD83C\uDF0E Source : <a href=\"${ans.meta.link}\">${ans.meta.source}</a>"

                    """
                        Q: ${ans.question}
                        A: ${ans.answer}
                        
                        💪 Answer Confidence : $confidence% $emoji
                        🌍 Source : <a href="${ans.meta.link}">${ans.meta.source}</a>
                    """.trimIndent()

                } else {
                    // Invalid query
                    "Sorry, I don't know about that"
                }
            }

            // Building feedback buttons
            val replyMarkup = if (modelId != null) {
                SendMessageRequest.ReplyMarkup(
                    listOf(
                        listOf(
                            SendMessageRequest.InlineButton(
                                FEEDBACK_RELEVANT_TEXT,
                                FEEDBACK_RELEVANT_KEY + modelId
                            ),

                            SendMessageRequest.InlineButton(
                                FEEDBACK_FAKE_TEXT,
                                FEEDBACK_FAKE_KEY + modelId
                            )
                        ),
                        listOf(
                            SendMessageRequest.InlineButton(
                                FEEDBACK_IRRELEVANT_TEXT,
                                FEEDBACK_IRRELEVANT_KEY + modelId
                            ),
                            SendMessageRequest.InlineButton(
                                FEEDBACK_OUTDATED_TEXT,
                                FEEDBACK_OUTDATED_KEY + modelId
                            )
                        )
                    )
                )
            } else {
                null
            }

            // Sending the message
            TelegramAPI.sendHtmlMessage(
                SecretConstants.ACTIVE_BOT_TOKEN,
                "${request.message.chat.id}",
                msg,
                request.message.messageId,
                replyMarkup
            )
        }.start()

    }
}