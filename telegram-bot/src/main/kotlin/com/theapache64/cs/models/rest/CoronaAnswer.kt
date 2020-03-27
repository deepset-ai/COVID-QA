package com.theapache64.cs.models.rest

import com.google.gson.annotations.SerializedName


class CoronaAnswer(
    @SerializedName("results")
    val results: List<Result>
)

data class Result(
    @SerializedName("answers")
    val answers: List<Answer>,
    @SerializedName("model_id")
    val modelId: Int,
    @SerializedName("question")
    val question: String // How does corona spread?
) {
    data class Answer(
        @SerializedName("answer")
        val answer: String, // It is not certain how long the virus that causes COVID-19 survives on surfaces, but it seems to behave like other coronaviruses. Studies suggest that coronaviruses (including preliminary information on the COVID-19 virus) may persist on surfaces for a few hours or up to several days. This may vary under different conditions (e.g. type of surface, temperature or humidity of the environment).If you think a surface may be infected, clean it with simple disinfectant to kill the virus and protect yourself and others. Clean your hands with an alcohol-based hand rub or wash them with soap and water. Avoid touching your eyes, mouth, or nose
        @SerializedName("context")
        val context: String, // It is not certain how long the virus that causes COVID-19 survives on surfaces, but it seems to behave like other coronaviruses. Studies suggest that coronaviruses (including preliminary information on the COVID-19 virus) may persist on surfaces for a few hours or up to several days. This may vary under different conditions (e.g. type of surface, temperature or humidity of the environment).If you think a surface may be infected, clean it with simple disinfectant to kill the virus and protect yourself and others. Clean your hands with an alcohol-based hand rub or wash them with soap and water. Avoid touching your eyes, mouth, or nose
        @SerializedName("meta")
        val meta: Meta,
        @SerializedName("offset_end")
        val offsetEnd: Int, // 642
        @SerializedName("offset_start")
        val offsetStart: Int, // 0
        @SerializedName("probability")
        val probability: Double, // 0.54761047
        @SerializedName("question")
        val question: String, // How long does the virus survive on surfaces?
        @SerializedName("score")
        val score: Double // 5.4761047
    ) {
        data class Meta(
            @SerializedName("answer_html")
            val answerHtml: String, // <p>It is not certain how long the virus that causes COVID-19 survives on surfaces, but it seems to behave like other coronaviruses. Studies suggest that coronaviruses (including preliminary information on the COVID-19 virus) may persist on surfaces for a few hours or up to several days. This may vary under different conditions (e.g. type of surface, temperature or humidity of the environment).</p><p>If you think a surface may be infected, clean it with simple disinfectant to kill the virus and protect yourself and others. Clean your hands with an alcohol-based hand rub or wash them with soap and water. Avoid touching your eyes, mouth, or nose.</p>
            @SerializedName("category")
            val category: String,
            @SerializedName("city")
            val city: String,
            @SerializedName("country")
            val country: String,
            @SerializedName("document_id")
            val documentId: Long, // 131
            @SerializedName("document_name")
            val documentName: String, // Q&A on coronaviruses (COVID-19)
            @SerializedName("lang")
            val lang: String, // en
            @SerializedName("last_update")
            val lastUpdate: String, // 2020/03/17
            @SerializedName("link")
            val link: String, // https://www.who.int/news-room/q-a-detail/q-a-coronaviruses
            @SerializedName("paragraph_id")
            val paragraphId: String, // zv7x7XABvTaZvFwu2OJO
            @SerializedName("question")
            val question: String, // How long does the virus survive on surfaces?
            @SerializedName("region")
            val region: String,
            @SerializedName("score")
            val score: String, // 5.4761047
            @SerializedName("source")
            val source: String // World Health Organization (WHO)
        )
    }
}