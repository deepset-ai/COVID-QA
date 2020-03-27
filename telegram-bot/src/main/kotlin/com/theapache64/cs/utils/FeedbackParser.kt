package com.theapache64.cs.utils

import com.theapache64.cs.models.Feedback

object FeedbackParser {
    private val feedbackRegEx = "(?<feedback>\\w)(?<modelId>\\d+)d(?<documentId>\\d+)(?<question>.+)".toRegex()
    fun parse(data: String): Feedback {
        val match = feedbackRegEx.find(data)
        val groups = match!!.groups
        return Feedback(
            groups["modelId"]!!.value.toInt(),
            getFeedbackString(groups["feedback"]!!.value[0]),
            groups["question"]!!.value,
            groups["documentId"]!!.value.toLong()
        )
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