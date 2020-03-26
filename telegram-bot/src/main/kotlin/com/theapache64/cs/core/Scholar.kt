package com.theapache64.cs.core

import com.theapache64.cs.models.rest.AddFeedbackRequest
import com.theapache64.cs.models.rest.CoronaAnswer
import com.theapache64.cs.models.rest.CoronaQuestion
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.RestClient

object Scholar {

    private const val BASE_URL = "https://covid-backend.deepset.ai"
    private const val MODEL_ID = "1"

    fun getAnswer(question: String): CoronaAnswer? {
        val jsonString = RestClient.post(
            "$BASE_URL/models/$MODEL_ID/faq-qa",
            null,
            CoronaQuestion(
                arrayOf(question)
            )
        ).body!!.string()

        println(jsonString)

        return GsonUtil.gson.fromJson(jsonString, CoronaAnswer::class.java)
    }

    fun addFeedback(documentId: Long, question: String, feedback: Char) {
        val feedbackString = getFeedbackString(feedback)
        val jsonString = RestClient.post(
            "$BASE_URL/models/$MODEL_ID/feedback",
            null,
            AddFeedbackRequest(feedbackString, question, documentId)
        ).body!!.string()
        println("Feedback response : $jsonString")
    }

    private fun getFeedbackString(feedback: Char): String {
        return when (feedback) {
            'r' -> "relevant"
            'f' -> "fake"
            'o' -> "outdated"
            'i' -> "irrelevant"
            else -> throw IllegalArgumentException("Undefined feedback char `$feedback`")
        }
    }
}