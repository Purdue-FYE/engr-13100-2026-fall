# Quizzes

Quiz questions are organized by concept (Excel, Modeling, Python etc.).  

For this directory to be used as a question bank, questions need to be written with a consideration towards page space. Questions should be written in multiples of half-pages.

Question writing should follow the typical contribution process so that reviewers can be assigned via pull requests.

## File Structure

Outermost folder: Question banks based on skill,(i.e. Excel, Modeling, Python)
Within there, folders indicate a topic, (i.e. Linear Regression, Spreadsheet Foundations)
Subfolders indicate detailed topics more closely aligned with learning objectives (i.e. Goodness of fit, Predictions, Scatter Plots)

Each question has its own markdown file. One question per file. Some questions have multiple parts. 

Question markdown files have descriptive names. 

When creating an exam, no more than one markdown file should be pulled from each sub-folder. 

All associated files linked within that markdown file should also be pulled. Associated files start with the same name as the markdown file, ending with a descriptor (ie, "img") and an appropriate extension.


## Typical Contribution Process

1. **Create a new branch**
   Each team member creates their own branch when working on an update or fix.

2. **Add Commits**
   Contributors only make commits to their own branch as work progresses.

3. **Rebase/Squash**
   Once the branch work is complete, the author should rebase their branch onto the main
   branch to ensure a clean history.  Minor commits should be squashed into logical
   units of work.

4. **Create a Pull Request**
   Once the commit history is clean, the author creates a pull request (PR) for review.

5. **Request Review**:
   The author should ask a team member to review their PR.

6. **Review the Pull Request**
   The reviewer checks the code for quality, standards, and correctness.  They should
   either approve the PR or request changes.  The reviewer does not merge the PR.

7. **Merge into main**
   Once the PR passes the review, the PR should be merged into the main branch by a
   member of a different team to maintain consistent standards across the teams.  The
   person merging must ensure only fast-forward merges are done (no merge commits).  If
   a rebase is required, rebasing should be done by the original author.