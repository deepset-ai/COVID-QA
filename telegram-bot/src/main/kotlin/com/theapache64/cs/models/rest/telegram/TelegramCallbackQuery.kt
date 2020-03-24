package com.theapache64.cs.models.rest.telegram

import com.google.gson.annotations.SerializedName


data class TelegramCallbackQuery(
    @SerializedName("callback_query")
    val callbackQuery: CallbackQuery,
    @SerializedName("update_id")
    val updateId: Int // 996097080
) {
    data class CallbackQuery(
        @SerializedName("chat_instance")
        val chatInstance: String, // -4027463488092007398
        @SerializedName("data")
        val `data`: String, // r123
        @SerializedName("from")
        val from: From,
        @SerializedName("id")
        val id: String, // 1034271309301426903
        @SerializedName("message")
        val message: Message
    ) {
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

        data class Message(
            @SerializedName("chat")
            val chat: Chat,
            @SerializedName("date")
            val date: Int, // 1584998447
            @SerializedName("from")
            val from: From,
            @SerializedName("message_id")
            val messageId: Long, // 61
            @SerializedName("reply_markup")
            val replyMarkup: ReplyMarkup,
            @SerializedName("text")
            val text: String // Was it helpful? 😊
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
                val firstName: String, // Corona Scholar - Dev
                @SerializedName("id")
                val id: Int, // 1119620721
                @SerializedName("is_bot")
                val isBot: Boolean, // true
                @SerializedName("username")
                val username: String // corona_scholar_dev_bot
            )

            data class ReplyMarkup(
                @SerializedName("inline_keyboard")
                val inlineKeyboard: List<Any>
            )
        }
    }
}