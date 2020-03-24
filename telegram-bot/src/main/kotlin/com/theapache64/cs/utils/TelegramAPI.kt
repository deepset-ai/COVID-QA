package com.theapache64.cs.utils

import com.theapache64.cs.models.rest.telegram.AnswerCallbackRequest
import com.theapache64.cs.models.rest.telegram.SendChatActionRequest
import com.theapache64.cs.models.rest.telegram.SendMessageRequest
import com.theapache64.cs.models.rest.telegram.SendMessageResponse
import java.io.IOException

object TelegramAPI {

    private const val BASE_URL = "https://api.telegram.org"


    /**
     * To send a text with Markdown
     */
    @Throws(IOException::class)
    fun sendHtmlMessage(
        from: String,
        to: String,
        message: String,
        replyMsgId: Long?,
        replayMarkup: SendMessageRequest.ReplyMarkup?
    ): SendMessageResponse {

        val url = "$BASE_URL/bot$from/sendMessage"

        val response = RestClient.post(
            url,
            null,
            SendMessageRequest(
                to,
                message,
                true,
                "HTML",
                replyMsgId,
                replayMarkup
            )
        )

        val respJsonString = response.body!!.string()
        if (response.code != 200) {
            throw IOException("Failed to send message '$message' -> $respJsonString")
        }
        return GsonUtil.gson.fromJson(respJsonString, SendMessageResponse::class.java)
    }

    fun answerCallbackQuery(
        from: String,
        id: String
    ) {
        val url = "$BASE_URL/bot$from/answerCallbackQuery"
        val resp = RestClient.post(
            url,
            null,
            AnswerCallbackRequest(id)
        ).body!!.string()

    }

    fun sendChatAction(
        from: String,
        chatId: String,
        action: String
    ) {
        val url = "$BASE_URL/bot$from/sendChatAction"
        val resp = RestClient.post(
            url,
            null,
            SendChatActionRequest(
                action,
                chatId
            )
        ).body!!.string()

    }
}