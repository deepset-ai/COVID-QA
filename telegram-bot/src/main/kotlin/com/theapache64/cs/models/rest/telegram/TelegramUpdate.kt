package com.theapache64.cs.models.rest.telegram

import com.google.gson.annotations.SerializedName


data class TelegramUpdate(
    @SerializedName("message")
    val message: Message,
    @SerializedName("update_id")
    val updateId: Int // 102073005
) {
    data class Message(
        @SerializedName("chat")
        val chat: Chat,
        @SerializedName("date")
        val date: Int, // 1584880886
        @SerializedName("from")
        val from: From,
        @SerializedName("message_id")
        val messageId: Long, // 8
        @SerializedName("text")
        val text: String // Dbrhrfjggkjgj nfgntnt t
    ) {
        data class Chat(
            @SerializedName("first_name")
            val firstName: String, // theapache64
            @SerializedName("id")
            val id: Int, // 240810054
            @SerializedName("type")
            val type: String, // private
            @SerializedName("username")
            val username: String // theapache64
        )

        data class From(
            @SerializedName("first_name")
            val firstName: String, // theapache64
            @SerializedName("id")
            val id: Int, // 240810054
            @SerializedName("is_bot")
            val isBot: Boolean, // false
            @SerializedName("language_code")
            val languageCode: String, // en
            @SerializedName("username")
            val username: String // theapache64
        )
    }
}