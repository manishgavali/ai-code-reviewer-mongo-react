MongoDB usage (collections)

Database: ai_code_reviewer_demo
Collection: reviews

Document schema (example):
{
  _id: ObjectId,
  repo: string | null,
  pr_number: int | null,
  files: [{ path: string, language: string, findings: {...} }],
  ai_summary: string | null,
  created_at: ISODate
}
