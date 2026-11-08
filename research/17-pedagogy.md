# 17. Pedagogy and computational thinking: carrying MIT's Scratch approach into Python

Research dimension: how MIT and Harvard teach with Scratch, what the research says about moving from blocks to text, and what that means for a 9-year-old who knows Scratch and is learning Python in Google Colab.

## Summary

1. **Teach the move explicitly.** Weintrop's research gives the main warning: when no one draws the links between blocks and text, children do not keep their block-based advantage once they move to text. Weintrop (2021) puts it as "transfer does not come for free". The fix with the best evidence is *mediated transfer* (Dann et al., 2012). Put the Scratch script and the Python next to each other and literally draw lines from each block to its Python line. Then ask the child to write the Python for a Scratch script they have not seen before. Every module of the workbook should have a side-by-side "Scratch block → Python line" panel and a "translate this script" exercise.
2. **Start every session with a project and give starter code to change.** Resnick's 4 Ps, the Brennan and Resnick practice of "reusing and remixing", Use-Modify-Create (Lee et al., 2011) and PRIMM (Sentance et al., 2019) all point the same way. The child should first *run and change* working code that makes something they care about. Writing from a blank cell comes later. Remixing in Python means: here is a cell that works; predict what it does, run it, change one thing, then add a feature.
3. **Put events and parallelism late in Python, not early as in Scratch.** In Scratch, events and parallelism come cheap ("when green flag clicked", many scripts running at once). In text languages they cost a lot. Dann et al. (2012) found that turning Alice code with events and concurrency into Java produced complex code too early. Python in Colab runs one line after another, and key and timer events need callback functions. So the module order should differ from Scratch's block-palette order. Sequence and turtle drawing come first, then loops, data and conditionals. Functions come before events and key presses.

## Key frameworks

### Resnick's 4 Ps of creative learning
From Resnick's Lifelong Kindergarten group at the MIT Media Lab (Resnick, 2014; 2017):
- **Projects:** people learn best while working on meaningful projects, not exercises.
- **Passion:** people who work on projects they care about keep going for longer and push through difficulty.
- **Peers:** learning is social. People share ideas, work together and build on each other's work.
- **Play:** this means playful experimenting, taking risks and trying things, not only "fun".

*For Python:* each module should end in a small thing the child can show someone (a drawing, a quiz, a game). Let the child choose the theme (football, animals, space). Make showing it to a parent or sibling part of the routine.

### Low floor, high ceiling, wide walls; tinkerability
Resnick et al. (2009) take "low floor, high ceiling" from Papert: easy to start, room to grow. They add **wide walls**, meaning support for many kinds of project. Scratch's design principles are to be more *tinkerable*, more *meaningful* and more *social*. The name "Scratch" itself refers to tinkering.

*For Python:* Colab plus a turtle library keeps the floor low (one cell, one line, a visible result). The walls are kept wide by offering several project types per concept: art, game, story, quiz.

### Brennan and Resnick (2012) computational thinking framework
**Concepts (7):** sequences, loops, events, parallelism, conditionals, operators, data.
**Practices (4):** being incremental and iterative; testing and debugging; reusing and remixing; abstracting and modularizing.
**Perspectives (3):** expressing (I can create with computation), connecting (I can create with and for others), questioning (I can ask how technology works and change it).

Points from the paper that matter for us:
- *Incremental and iterative:* design is a cycle of building a little, trying it, and building more. The interviewed child showed each finished level to her younger brother.
- *Testing and debugging:* the strategies children reported are worth teaching by name. Find where the problem is, read through your scripts, experiment, rewrite the script, look for a working example, tell someone about the problem, take a break.
- *Assessment:* their six suggestions are to support further learning, use projects, show the process, check in at several points along the way, value several ways of knowing, and include several viewpoints (for example a parent's). Their "design scenario" interview asked children to (1) explain what a project does, (2) describe how to extend it, (3) fix a bug and (4) remix it by adding a feature. This four-step check works well at the end of each module.

### Harvard Creative Computing Curriculum (Scratch 3.0 edition)
Brennan, Balch and Chung (2014; updated for Scratch 3.0). Seven units in this order:

| Unit | Theme | Concepts and practices emphasised |
|---|---|---|
| 0 | Getting Started | design journal, critique group, exploring |
| 1 | Exploring | **sequence** ("About Me" project) |
| 2 | Animations | **loops, events, parallelism** (music video) |
| 3 | Stories | **events, parallelism**; experimenting and iterating; reusing and remixing ("Pass It On") |
| 4 | Games | **conditionals, operators, data**; abstracting and modularizing |
| 5 | Diving Deeper | review, Know-Want-Learn self-check, debugging |
| 6 | Hackathon | plan-make-share cycle, "process over product" |

The guide gives no session times, and teachers are free to reorder activities. Two of its habits carry straight over to Python: a **design journal** (a paper notebook, or a text cell at the top of each Colab notebook), and **critique** (showing work to someone and getting feedback).

### Scratch Ideas and Coding Cards
The Official Scratch Coding Cards (Rusk, 2019) are 75 cards, each a short project with the code on the back, built around sequencing, conditionals and variables. Their format (one small goal, picture of the result, minimal code, "try this" extensions) is a good model for workbook pages.

### Use-Modify-Create and PRIMM
- **Use-Modify-Create** (Lee et al., 2011): learners first use a working artefact, then modify it, then create their own. This is the classroom form of "reusing and remixing".
- **PRIMM** (Sentance, Waite and Kallia, 2019; Raspberry Pi Foundation): Predict, Run, Investigate, Modify, Make. It is built on reading and tracing code before writing it, and it was designed for school text-based programming, usually Python.

## Evidence on block-to-text transition

| Study | Setting | Finding | What it means for us |
|---|---|---|---|
| Weintrop and Wilensky (2015) | High school, Snap! vs text questions | Students did better on block questions about conditionals, function calls and definite loops. There was no difference for variables, indefinite loops or reading programs. | Expect `if` syntax, `for` loops and calling functions to feel harder in text. Spend extra translation practice on these. |
| Weintrop and Wilensky (2017) | 5 weeks, matching block vs text (Pencil.cc), high school | Both groups improved. The block group gained more and was more interested in future courses. The text group felt more like "real programmers". Confidence and enjoyment were the same. Students rated conditionals and loops as easier in blocks. | A child who moves to text can enjoy it just as much. Feeling like a "real programmer" motivates, so name and celebrate it. |
| Weintrop and Wilensky (2019) | Same students after 10 weeks of Java | The early block advantage faded. Achievement and attitudes were the same whichever tool they started with. The teacher used **no bridging strategies**. | Knowing Scratch does not by itself make Python easier. The adult has to make the connections. |
| Weintrop (2021), RPF seminar | Summary chapter | "Transfer does not come for free". Explicit teaching that links blocks to keywords helps. He recommends dual-modality tools (Pencil Code, frame-based editing) and asking whether to use blocks or text is a false choice. | Use side-by-side translation. A dual view (EduBlocks) is a fair bridge. |
| Dann et al. (2012) | University CS1, Alice 3 → Java over two years | Mediated-transfer sections scored at least one letter grade higher. The two techniques: **bridging** (analogies, generalising a concept into new contexts) and **hugging** (making the learning task look like the target task: blocks and Java on screen at once, with lines drawn between equivalent statements, then translating new code on paper). Events and concurrency were the hardest parts to carry over. | The best-supported concrete method. Use it in every module. Put events and parallelism late. |
| Armoni, Meerbaum-Salant and Ben-Ari (2015) | Israeli middle school Scratch → secondary C#/Java | Students with Scratch experience learned new topics in less time and had fewer difficulties. Earlier work by the same group warned that Scratch can build bad habits (for example, very fine-grained scripts and little planning). | Scratch background is a real asset. Teach planning before coding, and one-script-per-job, early on. |
| Altadmri and Brown (2015) | 37 million Java compile events from beginners (Blackbox) | Beginners make the same few mistakes again and again, and teachers' guesses about which mistakes are common are often wrong. | Keep a "my common errors" list for this child and look for patterns. Do not assume which errors will happen. |
| Raspberry Pi Foundation, "Scratch to Python" course and "Paint with Python" (Scott, 2024) | For teachers and volunteers of ages 7 to 14 | Compare syntax side by side, convert Scratch programs to Python, and treat error types explicitly. Paint with Python starts with choosing from options, then moves to typing small snippets. A lot of code is pre-written. Error feedback is clear. Learning is self-paced. | Confirms starter code, small typed changes and a gradual shift from clicking to typing. |

**Transition tools**
- **EduBlocks** (Joshua Lowe; now hosted by Anaconda): Scratch-style blocks with the matching Python shown live beside them, one block per line. Good as a *short* bridge (one or two sessions per module, or whenever a concept is stuck). It is not where the child should stay.
- **BlockPy** (Bart et al., University of Delaware): a dual block/text Python environment with autograding, so the learner can switch views.
- **Pencil Code** (Bau et al., 2015): a dual-modality editor. It was the text-equivalent environment family used in the Weintrop studies.
- Evidence: dual-modality tools are promising (Weintrop, 2021, citing Matsuzawa et al., 2015 and Blanchard et al., 2020). No study shows that they beat well-run side-by-side teaching in plain text. Treat them as an extra support, not the main method.

## Practical rules for this learner

These rules turn the evidence above into practice. Where a rule is practitioner judgement, not a research finding, it is marked *(judgement)*.

1. **Project first, concept second.** Open each session with "today we will make X" and show the finished result. Bring in the concept when the project needs it, as Brennan and Resnick's game example does (a child wants a score, so it is time for variables). Never start with "today: variables".
2. **Remix before writing (PRIMM / Use-Modify-Create).** Each Colab notebook gives a working starter cell. The routine: *Predict* (say what it will do), *Run*, *Investigate* (what does this line do?), *Modify* (change one number, colour or word), *Make* (add one feature of your own). Writing from a blank cell comes at the end of a module, never at the start.
3. **Always show Scratch next to Python (hugging).** Each new construct gets a picture of the Scratch block next to the Python line, with arrows. Each module includes at least one "here is a Scratch script; write it in Python" task, done on paper or in a cell (Dann et al., 2012). Name analogies out loud as bridging ("`for i in range(4):` is the `repeat 4` block, and the indent is the C-shaped mouth").
4. **Short sessions with something working at the end** *(judgement; the guides give no times)*. Plan 30 to 45 minutes, and end on something that runs and can be shown. Stop before frustration builds. Brennan and Resnick list "take a break" as a real debugging strategy, so teach it as one.
5. **Typing speed: keep typing small and the code pre-written.** Following Paint with Python, keep the amount a 9-year-old has to type per session to a few lines. Give the boilerplate (imports, setup) in a hidden or "don't touch" cell. Let the child edit values first and write new lines later. Copy-paste from a Python "block palette" cell is allowed (it is the text form of dragging a block). Encourage typing practice outside coding sessions *(judgement)*.
6. **Make errors a game, not a failure.** Teach a short routine based on the strategies Scratchers reported: read the last line of the red error, find the line number, compare with the example, ask someone, take a break. Keep a "bug collection" page of this child's own common errors: missing colon, wrong indent, unclosed quote, capital letters (Altadmri and Brown, 2015: track the errors that actually happen).
7. **The parent is a coach and audience, not the typist.** Ask the questions from Brennan and Resnick's four-step check ("What does it do? How could you extend it? Can you fix this bug? Add a feature"). Be the critique group. Let the child explain the code to you (showing the process). Avoid taking the keyboard *(judgement)*. Celebrate "you are writing code like real programmers do", since this feeling was a measured motivator (Weintrop and Wilensky, 2017).
8. **Passion and wide walls.** Offer two or three themes for each project. Let the child rename variables and pick colours, words and characters.
9. **Design journal.** A text cell (or a paper notebook) at the top of each notebook, with the headings "What I want to make / What I changed / What went wrong / What I'll try next". This covers the incremental-and-iterative practice and makes the process visible for assessment.
10. **When to use EduBlocks** *(judgement informed by Weintrop, 2021)*. Use it (a) in the first session or two to show that blocks and Python are the same thing, (b) whenever a construct is stuck after two tries in text (for example nested `if`/`else` or loops), and (c) for a one-off "build it in blocks, read the Python" task. Then come back to Colab. Do not make it the main environment, because the goal is fluency in text.
11. **Don't wait for Scratch to transfer by itself.** Weintrop and Wilensky (2019) found no lasting advantage when teaching gave no bridges. Each module needs explicit "this is the Python for that block" teaching.
12. **Check in at several points along the way, without tests.** At the end of each module, use the design-scenario check: explain, extend, debug, remix a short program. There are no quizzes on definitions (Brennan and Resnick, Suggestion 5: knowing what a loop *is* is not enough).

## Recommended module order

The 8 workbook modules follow Scratch's block palette. The research suggests a **different order** for Python, for two reasons:
- The Creative Computing Curriculum goes from sequence, to loops, events and parallelism, then to conditionals, operators and data. That fits Scratch, where events and parallelism are free.
- In Python, events and parallelism are the *hardest* parts to carry over (Dann et al., 2012). In Colab they need callback functions and an interactive drawing backend. Functions should therefore come *before* events and key presses.

Turtle drawing is a natural first step: it gives instant visible feedback (low floor), it matches the Scratch pen/motion blocks the child already knows, and it continues Papert's Logo tradition, which Scratch itself comes from.

| # | Module (workbook name) | CT concept (Brennan and Resnick) | Why here |
|---|---|---|---|
| 1 | **Motion/turtle** (+ the "say" part of Looks as `print`) | sequences | Lowest floor, visible result straight away, direct match to Scratch motion and pen blocks. "Run cell" plays the part of the green flag, so no real event handling is needed yet. |
| 2 | **Control, part A: loops** (`repeat` → `for`, `forever` → `while True` with care) | loops | Comes up naturally from drawing shapes. Weintrop's data say loop syntax is harder in text, so practise it early and often. |
| 3 | **Variables and lists** | data | Score, name, size of shape. Motivated by the project (Brennan and Resnick's score example). |
| 4 | **Operators** | operators | Maths, joining text, random numbers, comparisons. These are needed for the next module. |
| 5 | **Sensing + Control, part B: conditionals** (`ask and wait` → `input()`, `if`/`else`) | conditionals | Quiz and guessing-game projects. Comes after operators because comparisons are needed. Matches Creative Computing Unit 4 (Games: conditionals, operators, data). |
| 6 | **Functions** (My Blocks → `def`) | abstracting and modularizing | Matches the Games unit's focus on abstraction. Needed before event callbacks. Function calls were harder in text (Weintrop and Wilensky, 2015), so give this module time. |
| 7 | **Events, Looks extras, sound and key presses** (when key pressed → `onkey` callback, broadcast → calling a function, play sound → `IPython.display.Audio`) | events, parallelism | Hardest to carry over. It builds on functions. Check what the Colab turtle library supports for key events (other research files cover this). |
| 8 | **Hackathon/remix project** | all practices | Mirrors Creative Computing Unit 6: plan-make-share, process over product, a project of the child's own design to show the family. |

If the workbook's existing module numbering has to stay, keep it but **teach in the order above**. As a minimum: (a) take "events" out of Module 1 apart from "run cell = green flag", (b) teach functions before key presses and sound events, and (c) teach loops before variables, because drawing shapes needs `repeat` straight away.

## Sources

- Altadmri, A., & Brown, N. C. C. (2015). 37 million compilations: Investigating novice programming mistakes in large-scale student data. *Proceedings of the 46th ACM Technical Symposium on Computer Science Education (SIGCSE '15)*, 522–527. https://doi.org/10.1145/2676723.2677258 . Repository: https://kar.kent.ac.uk/46742
- Armoni, M., Meerbaum-Salant, O., & Ben-Ari, M. (2015). From Scratch to "real" programming. *ACM Transactions on Computing Education, 14*(4), Article 25. Project page: https://weizmann.ac.il/ScienceTeaching/research-and-development/computer-science/projects/685
- Bart, A. C., et al. BlockPy: dual block/text Python environment. https://blockpy.cis.udel.edu/
- Bau, D., Bau, D. A., Dawson, M., & Pickens, C. S. (2015). Pencil Code: Block code for a text world. *Proceedings of the 14th International Conference on Interaction Design and Children*, 445–448. https://pencilcode.net/
- Brennan, K., Balch, C., & Chung, M. (2014; Scratch 3.0 edition). *Creative Computing Curriculum*. Harvard Graduate School of Education. https://creativecomputing.gse.harvard.edu/guide/curriculum.html
- Brennan, K., & Resnick, M. (2012). New frameworks for studying and assessing the development of computational thinking. Paper presented at the Annual Meeting of the American Educational Research Association, Vancouver, Canada. https://scratched.gse.harvard.edu/ct/files/AERA2012.pdf
- Dann, W., Cosgrove, D., Slater, D., Culyba, D., & Cooper, S. (2012). Mediated transfer: Alice 3 to Java. *Proceedings of the 43rd ACM Technical Symposium on Computer Science Education (SIGCSE '12)*, 141–146. PDF: https://www.alice.org/wp-content/uploads/2017/04/MediatedTransfer.pdf
- EduBlocks (J. Lowe; Anaconda). https://edublocks.org/ ; Computing at School overview: https://www.computingatschool.org.uk/resources/2025/november/edublocks-from-blocks-to-text/
- Lee, I., Martin, F., Denner, J., Coulter, B., Allan, W., Erickson, J., Malyn-Smith, J., & Werner, L. (2011). Computational thinking for youth in practice. *ACM Inroads, 2*(1), 32–37. https://doi.org/10.1145/1929887.1929902
- Raspberry Pi Foundation and NCCE. *Scratch to Python: Moving from block- to text-based programming* (online course for teachers of 7–14 year olds). https://training-hub.raspberrypi.org/en/courses/teach-computing-moving-from-scratch-to-python
- Raspberry Pi Foundation (2023). *Pedagogy quick read: PRIMM*. https://static.raspberrypi.org/files/curriculum/quickreads/11-Pedagogy_Summary_PRIMM_V4_2023.pdf
- Resnick, M. (2014). Give P's a chance: Projects, peers, passion, play. *Constructionism and Creativity conference*, Vienna. https://web.media.mit.edu/~mres/papers/constructionism-2014.pdf
- Resnick, M. (2017). *Lifelong Kindergarten: Cultivating Creativity through Projects, Passion, Peers, and Play*. MIT Press.
- Resnick, M., Maloney, J., Monroy-Hernández, A., Rusk, N., Eastmond, E., Brennan, K., Millner, A., Rosenbaum, E., Silver, J., Silverman, B., & Kafai, Y. (2009). Scratch: Programming for all. *Communications of the ACM, 52*(11), 60–67. https://web.media.mit.edu/~mres/papers/Scratch-CACM-final.pdf
- Rusk, N. (2019). *The Official Scratch Coding Cards (Scratch 3.0): Creative Coding Activities for Kids*. No Starch Press. ISBN 9781593279769.
- Scott, M. (2024, August 28). Bridging the gap from Scratch to Python: Introducing "Paint with Python". Raspberry Pi Foundation blog. https://www.raspberrypi.org/blog/learn-to-code-python/
- Sentance, S., Waite, J., & Kallia, M. (2019). Teaching computer programming with PRIMM: A sociocultural perspective. *Computer Science Education, 29*(2–3), 136–176. https://doi.org/10.1080/08993408.2019.1608781
- Weintrop, D. (2021). The role of block-based programming in computer science education. In *Understanding computing education (Vol. 1): Proceedings of the Raspberry Pi Foundation Research Seminars*. https://terpconnect.umd.edu/~weintrop/papers/Weintrop_RaspPi_2021.pdf
- Weintrop, D., & Wilensky, U. (2015). Using commutative assessments to compare conceptual understanding in blocks-based and text-based programs. *Proceedings of the 11th Annual ACM International Computing Education Research Conference (ICER '15)*, 101–110. (Finding as summarised in Weintrop & Wilensky, 2017, §2.2; full text not retrieved.)
- Weintrop, D., & Wilensky, U. (2017). Comparing block-based and text-based programming in high school computer science classrooms. *ACM Transactions on Computing Education, 18*(1), Article 3. https://doi.org/10.1145/3089799 . PDF: https://ccl.northwestern.edu/2017/a3_weintrop_wilensky.pdf
- Weintrop, D., & Wilensky, U. (2019). Transitioning from introductory block-based and text-based environments to professional programming languages in high school computer science classrooms. *Computers & Education, 142*, 103646. https://doi.org/10.1016/j.compedu.2019.103646 . PDF: https://www.terpconnect.umd.edu/~weintrop/papers/Weintrop&Wilensky_2019_C&E.pdf

*Verification note:* I read the full text of Brennan and Resnick (2012), Weintrop and Wilensky (2017), Weintrop (2021) and Dann et al. (2012). Weintrop and Wilensky (2019), Armoni et al. (2015), Altadmri and Brown (2015), PRIMM and the Resnick 2009 and 2014 papers come from abstracts, highlights or secondary summaries. The Weintrop and Wilensky (2015) finding comes from the literature review in their 2017 paper. Times and parent-role rules marked *(judgement)* are not research findings.
