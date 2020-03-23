package com.theapache64.cs.core

import com.theapache64.cs.models.AddFeedbackRequest
import com.theapache64.cs.models.CoronaAnswer
import com.theapache64.cs.models.CoronaQuestion
import com.theapache64.cs.utils.GsonUtil
import com.theapache64.cs.utils.RestClient

object Scholar {

    private const val ANSWER_ENDPOINT = "https://covid-middleware.deepset.ai/api/bert/question"
    private const val KEY_MODEL_ID = "{modelId}"
    private const val FEEDBACK_ENDPOINT_FORMAT = "http://3.121.62.187/models/$KEY_MODEL_ID/doc-qa"

    fun getAnswer(question: String): CoronaAnswer? {
        val jsonString = RestClient.post(
            ANSWER_ENDPOINT,
            null,
            CoronaQuestion(question)
        ).body!!.string()

        return GsonUtil.gson.fromJson(jsonString, CoronaAnswer::class.java)
    }

    fun addFeedback(modelId: String, feedback: Char) {
        val feedbackString = getFeedbackString(feedback)
        val url = FEEDBACK_ENDPOINT_FORMAT.replace(KEY_MODEL_ID, modelId)
        val jsonString = RestClient.post(
            url,
            null,
            AddFeedbackRequest(feedbackString)
        ).body!!.string()
        println("Feeback response : $jsonString")
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