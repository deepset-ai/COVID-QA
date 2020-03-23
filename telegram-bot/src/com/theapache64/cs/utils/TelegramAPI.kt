package com.theapache64.cs.utils

import com.theapache64.cs.models.SendMessageRequest
import com.theapache64.cs.models.SendMessageResponse
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
        replyMsgId: Long?
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
                replyMsgId
            )
        )

        val respJsonString = response.body!!.string()
        if (response.code != 200) {
            throw IOException("Failed to send message '$message' -> $respJsonString")
        }
        return GsonUtil.gson.fromJson(respJsonString, SendMessageResponse::class.java)
    }
}