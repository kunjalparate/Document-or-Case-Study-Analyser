{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "a8f87fb3-dbd9-455a-9891-b7ad2239353e",
   "metadata": {},
   "outputs": [],
   "source": [
    "SYSTEM_PROMPT = (\n",
    "    \"You are a meticulous business strategy analyst. You read long case studies, \"\n",
    "    \"separate signal from noise, and produce crisp, structured, actionable analysis. \"\n",
    "    \"Keep writing concise but complete. Use bullet points where helpful.\"\n",
    ")\n",
    "\n",
    "FIRST_PASS_PROMPT = (\n",
    "    \"You will receive a case study text. Perform a first-pass distillation.\\n\\n\"\n",
    "    \"Return JSON with keys: background, problem_statement, stakeholders, key_facts, constraints.\\n\"\n",
    "    \"- key_facts must include numbers, dates, KPIs, and any financial figures as plain text.\\n\"\n",
    ")\n",
    "\n",
    "STRUCTURED_ANALYSIS_PROMPT = (\n",
    "    \"Using the distilled info, produce: (1) Executive Summary (150-250 words),\\n\"\n",
    "    \"(2) SWOT, (3) If relevant: PESTEL, (4) 3-5 Actionable Recommendations with rationale,\\n\"\n",
    "    \"(5) Assumptions & Missing Information, (6) Risks & Mitigations.\\n\"\n",
    ")\n",
    "\n",
    "REFINEMENT_PROMPT = (\n",
    "    \"Refine the analysis for clarity, de-duplication, and prioritization.\\n\"\n",
    "    \"- Tighten language, remove fluff, and ensure recommendations are prioritized with impact and effort.\\n\"\n",
    ")\n",
    "\n",
    "REPORT_PROMPT = (\n",
    "    \"Format a final report in Markdown with the following sections:\\n\"\n",
    "    \"# Executive Summary\\n# Situation Overview\\n# Problem Statement\\n# Stakeholders\\n# Key Facts & Figures\\n# SWOT Analysis\\n# PESTEL (if applicable)\\n# Recommendations (Prioritized)\\n# Assumptions & Information Gaps\\n# Risks & Mitigations\\n\\n\"\n",
    "    \"Where possible, use bullet points and short paragraphs.\"\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c09f11bf-2a2c-4baa-8407-a23334a8d861",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
