# terms_batch1_rows.py
# Version 1.2 (pre-print verification FIX2: Waldron quotes checked by OCR, named laws by web check)
# Source rows for the artful-terms Leitner deck, batch 1: fallacies, argument forms and moves of reasoning,
# Waldron/Cammarata writing moves, and named heuristics/laws. Writes artful-terms-batch1.csv (UTF-8 with BOM).
# Fields: id, class, term, gloss, form, use, example, source, notes
#   class   : fallacy | form | move | heuristic   (printed as the small tag on the card front)
#   gloss   : what it is, one line
#   form    : general form / template (fallacies, forms, moves); blank where the gloss already is the form
#   use     : when to reach for it
#   example : a concrete case, from our chats where one fits; printed on the front of the "name it" card
#   source  : where the term/gloss/example came from (audit trail)
import csv, sys

R = []
def row(cls, term, gloss, form, use, example, source, notes=""):
    R.append(dict(cls=cls, term=term, gloss=gloss, form=form, use=use, example=example, source=source, notes=notes))

# ---------------- FALLACIES ----------------
F = "fallacy"
row(F, "genetic fallacy", "judging a claim by where it came from, not by its content",
    "X comes from S; S is suspect; so X is false", "someone discredits an idea by its origin",
    "“The Heart Sutra was composed in China, so it shouldn’t carry the same weight.”", "chat: Heart Sutra test, Oct 14")
row(F, "argument from silence", "inferring from what a source fails to mention",
    "S doesn’t mention X; so X is absent or false", "an absence is offered as evidence; ask whether S would have mentioned X",
    "“The Nikāyas never teach emptiness this way, so it must be a later invention.”", "chat: Heart Sutra test, Oct 14",
    "weak evidence of lateness, no evidence of falsity")
row(F, "special pleading", "applying a standard to others while exempting your own case",
    "standard D rules out A; B also fails D; B is kept anyway", "a rule is applied unevenly",
    "“Late editing disqualifies the Laṅkāvatāra” — though the Pāli suttas were edited late too.", "chat: vegetarian test, Oct 14")
row(F, "appeal to popularity", "taking wide acceptance as proof (argumentum ad populum)",
    "many believe or do P; so P is true", "a crowd is offered as evidence; ask what the crowd is evidence of",
    "“Every Mahāyāna monastery chants it daily, so it can’t be unreliable.”", "chat: Heart Sutra test, Oct 14",
    "popularity is real evidence of received authority, not of origin")
row(F, "appeal to tradition", "taking long custom as proof that something is right",
    "we have always done P; so P is right", "“that’s how it’s done” is the whole argument",
    "“We’ve always chanted it this way, so this way is correct.”", "standard catalogue")
row(F, "appeal to authority", "citing an authority outside their field, or as if citing settled a question",
    "A says P; so P", "the weight rests on the speaker, not the reasons; legitimate when A is expert on P",
    "“A famous physicist says Yogācāra is idealism, so it is.”", "standard catalogue")
row(F, "ignoratio elenchi", "missing the point: a sound argument for a different conclusion",
    "Q is argued when P is at issue", "a reply is true but answers a question nobody asked",
    "Housing: “the current LEDs are already the most energy-efficient option” — the request was about colour, not energy.", "chat: Housing test, Oct 20")
row(F, "equivocation", "a word shifts meaning partway through an argument",
    "premise true in sense 1; conclusion needs sense 2", "a key word is doing two jobs; split it into its senses",
    "“Authentic” slides from ‘composed in India’ to ‘authoritative’ to ‘true’.", "chat: Heart Sutra review, Oct 14")
row(F, "false dilemma", "offering two options as if they were the only ones",
    "A or B; not A; so B", "a choice feels forced; look for the third option",
    "“Should I just drop Anki and read more?”", "chat: Anki test, Oct 14")
row(F, "hasty generalization", "a broad conclusion from too few cases",
    "a few cases are X; so all are X", "one striking example carries a general claim",
    "One essay sounds like our chats, so “our language is shifting.”", "chat: Cammarata essay, Oct 17")
row(F, "post hoc ergo propter hoc", "treating a sequence in time as proof of cause",
    "A, then B; so A caused B", "only timing links the two; as a hypothesis to test it is fine (abduction)",
    "“The style dropped right after I asked for plain speech, so that request caused it.”", "chat: Nov 1",
    "Xiu offered it as a hypothesis, which is legitimate")
row(F, "affirming the consequent", "a formal fallacy: running a conditional backwards",
    "if P then Q; Q; so P", "a sign that fits is taken as proof of its usual cause",
    "“AI-polished text is precise; this essay is precise; so AI polished it.”", "chat: Cammarata essay, Oct 17")
row(F, "denying the antecedent", "a formal fallacy: negating the condition to negate the result",
    "if P then Q; not P; so not Q", "a sufficient condition is treated as the only one",
    "“If it’s in the Pāli canon it’s the Buddha’s word; this isn’t, so it isn’t.”", "constructed")
row(F, "begging the question", "assuming the very thing in dispute (petitio principii)",
    "P, because (P restated)", "the premise only persuades someone who already agrees",
    "Telling a Theravādin “origin isn’t authority” — the very criterion he rejects.", "chat: vegetarian review, Oct 14")
row(F, "non sequitur", "a conclusion that doesn’t follow from its premises",
    "P; so Q (no link shown)", "the ‘so’ is doing all the work",
    "“Gibson’s book is built around reading, so Anki time is wasted.”", "chat: Anki test, Oct 14",
    "Gibson’s own site offers a 2,000-card Anki deck")
row(F, "guilt by association", "rejecting a claim because of who else holds it",
    "a bad person holds P; so P is wrong", "a proposal is judged by its proposer",
    "“Devadatta proposed vegetarianism, and he tried to kill the Buddha.”", "chat: vegetarian test, Oct 14")
row(F, "fallacy of composition", "assuming what holds for a part holds for the whole",
    "each part is F; so the whole is F", "one step is doable, so the whole project must be",
    "“REA can read firmware, so I can jailbreak my phone.”", "chat: REA test, Oct 14")
row(F, "fallacy of division", "assuming what holds for the whole holds for each part",
    "the whole is F; so each part is F", "a group’s quality is pinned on a member",
    "“The saṅgha is wise, so this monk is wise.”", "constructed")
row(F, "straw man", "rebutting a weaker version than the one actually held",
    "they hold P; you refute P′ (weaker); you claim P refuted", "the rebuttal is easy; check it against their real claim",
    "“Reading is recognition, so his premise supports Anki” — he meant recognition on a card.", "chat: Anki review, Oct 14")
row(F, "slippery slope", "claiming one step must lead to an extreme without showing the chain",
    "if A, then B, then … Z; Z is terrible; so not A", "a chain of consequences is asserted, not argued",
    "“If one building changes its bulbs, soon every building will rewire its fixtures.”", "constructed; contrast floodgates")
row(F, "fallacy fallacy", "concluding a claim is false because an argument for it is bad",
    "the argument for P is fallacious; so not P", "you’ve just named a fallacy; the conclusion may still be true",
    "“His argument from silence fails, so the Heart Sutra must be early.”", "chat: logic rule, Oct 14")

# ---------------- FORMS AND MOVES OF REASONING ----------------
V = "form"
row(V, "modus ponens", "a valid form: affirming the condition",
    "if P then Q; P; so Q", "checking that an argument’s skeleton is sound",
    "If the tubes are Type B, they need a ballast-bypass replacement; they are; so they do.", "chat: Housing test, Oct 20")
row(V, "modus tollens", "a valid form: denying the result",
    "if P then Q; not Q; so not P", "testing a claim by a consequence that fails",
    "“If we allow you, we must allow everyone; we can’t allow everyone; so we can’t allow you.”", "chat: Housing test, Oct 20")
row(V, "disjunctive syllogism", "a valid form: eliminating one of two options",
    "P or Q; not P; so Q", "valid only if the two options really exhaust the field (else false dilemma)",
    "The ink fades either because of the toner or the paper; the toner is new; so it’s the paper.", "constructed")
row(V, "reductio ad absurdum", "assume the claim, derive something absurd, reject the claim",
    "suppose P; P leads to absurd R; so not P", "showing an argument proves too much",
    "“By your logic, forest-dwelling and rag-robes are tainted too — Devadatta proposed them.”", "chat: vegetarian review, Oct 14")
row(V, "a fortiori", "“all the more so”: if it holds in the stronger case, it holds in the weaker",
    "if even X, then all the more Y", "a point already made covers an easier case",
    "Even at full use the energy difference is small; with the lights on briefly each week, all the more.", "chat: Housing test, Oct 20")
row(V, "abduction", "inference to the best explanation: a hypothesis put forward to be tested",
    "Q is observed; P would explain Q; so P is worth testing", "proposing a cause without claiming proof",
    "“The style dropped after the Health thread — maybe that request leaked.”", "chat: Nov 1")
row(V, "enthymeme", "an argument with a premise left unstated",
    "P; so Q (missing: if P then Q)", "find the suppressed premise, state it, then test it",
    "Housing’s precedent reply rests on an unstated “we can’t judge requests one at a time.”", "chat: Housing review, Oct 20")
row(V, "floodgates argument", "granting one case obliges granting every like case",
    "allowing A requires allowing all like A; that is unmanageable; so not A", "a consistency objection; answer the premise, not the logic",
    "Housing: “if we let you change the bulbs, we’d have to let every building.”", "chat: Housing test, Oct 20",
    "differs from slippery slope: the link is consistency, not a causal chain")
row(V, "internal critique", "arguing from premises the other side already accepts",
    "by your own standard S, your claim fails", "you need to persuade them, not yourself",
    "Gibson’s own 2,000-card Anki deck, against “Gibson is reading-based, so drop Anki.”", "chat: Anki test, Oct 14")
row(V, "principle of charity", "interpret a claim in its strongest reasonable form before testing it (steelmanning)",
    "", "before any rebuttal, including of your own sentences",
    "Reading “I’m tired because I didn’t sleep” as the difference-maker, not the whole cause.", "chat: Oct 20 (Neil Wilson 1959; Quine, Davidson)")
row(V, "low diagnosticity", "evidence about as likely under the rival explanation, so it barely moves the odds",
    "E is likely if H and likely if not-H; so E says little about H", "a sign fits your theory and every other theory too",
    "Precise prose is weak evidence of AI: strong human writers write precisely too.", "chat: Cammarata essay, Oct 17")
row(V, "peritrope", "a thesis that refutes itself when applied to itself",
    "“all X are Y” is itself an X that isn’t Y", "a universal claim covers itself",
    "“All claims are relative” — including that one?", "Lexicon: Self-reference")

# ---------------- WRITING MOVES (Waldron, Cammarata) ----------------
M = "move"
row(M, "contrastive compression", "fold a whole shift into one “from X to Y” sentence",
    "from X to Y; not X but Y", "summarising a historical or conceptual change",
    "“From deconstructing essences logically to showing how to stop imputing them psychologically.”", "Waldron, Making Sense of Mind Only (prologue/intro sample)")
row(M, "grammatical reframe", "change the question’s grammar or aspect to change what can be asked",
    "‘what is X?’ → ‘how does X come about?’; noun → verb", "a question keeps producing essences",
    "“The neuron is better understood as a verb than a noun.”", "Cammarata; Waldron p. 26 (transposed questions)")
row(M, "coined handle", "name a recurring tension once, then reuse the name",
    "“what we will call the ___”", "a problem keeps returning in different guises",
    "“What we will call the Abhidharma Problematic.”", "Waldron p. 78–84; Cammarata “recursive generalization”")
row(M, "relocated boundary", "move a line instead of denying it exists",
    "the line runs not between A and B, but between C and D", "a dichotomy is felt but drawn in the wrong place",
    "The private/shared line runs “not between our skin-encapsulated body and the world, but between our material senses and our ‘minds’.”", "Waldron p. 231")
row(M, "inline gloss", "give a technical term its meaning, and its original, in passing",
    "term (original): short gloss", "introducing a term without stopping the sentence",
    "“Each dharma was defined in terms of its own-being (svabhāva).”", "Waldron p. 77")
row(M, "strong/weak split", "divide a loaded term into its strong and weak senses before arguing",
    "X in the strong sense vs. X in the weak sense", "an argument trades on one word",
    "“Depend upon mind”: a strong ontological dependence vs. a weaker epistemological one.", "Waldron p. 14")
row(M, "claim classification", "say what kind of claim it is before weighing it",
    "this is a metaphor / remedy / definition, not an explanation / assertion", "a sentence is being judged by the wrong standard",
    "The seed “is a metaphor (not a dharma)”; Milinda’s similes “do not explain” continuity.", "Waldron pp. 39, 97")
row(M, "etymology as argument", "unpack a word’s parts when they carry the claim",
    "split at the morpheme: in-dependent, de-sign-ate, vi-jñāna", "the word’s structure already says the point",
    "vi- ‘division’ in vijñāna: awareness arises by contrast, like noticing the fridge hum only when it stops.", "Waldron pp. 42, 56–57, 79")
row(M, "paired axes", "set two contrasting axes to place things precisely",
    "synchronic / diachronic; basis / object of analysis", "a question mixes two dimensions",
    "Taking separateness “as the basis of analyzing our experience rather than as the object of that analysis.”", "Waldron pp. 55, 86")
row(M, "parallel adverbs", "sort a doctrine’s aims with a set of matched adverbs",
    "thinking Xly, Yly, Zly", "one teaching serves several purposes at once",
    "The Buddha was thinking remedially, causally, soteriologically.", "Waldron p. 160")
row(M, "modern witness", "set a modern finding beside the classical text",
    "classical claim + modern field’s parallel", "showing an old idea is not merely old",
    "Vasubandhu’s fused atoms beside the binding problem; afflicted mind beside the rubber-hand illusion.", "Waldron pp. 217, 262")
row(M, "rival predictions", "set two hypotheses against what each would predict",
    "if H1, expect E; if H2, expect not-E", "two explanations both sound right",
    "“Recursive generalization and superposition predict nearly opposite things.”", "Cammarata")
row(M, "confidence label", "state how sure you are, explicitly",
    "Highly speculative: … / Confident: …", "a bold claim sits beside solid ones",
    "“Highly speculative: this might be most of what we need.”", "Cammarata")
row(M, "empty-explanation check", "expose an explanation that fits every outcome and so predicts nothing",
    "its only evidence is that something is unexplained", "a theory can never lose",
    "“Superposition’s only symptom is that something doesn’t make sense.”", "Cammarata")
row(M, "burden inversion", "show a view was made the default when it should have been the last resort",
    "X was the null hypothesis when it should have been the last", "a field’s starting assumption went unexamined",
    "“Making superposition the null hypothesis when it should have been the last hypothesis.”", "Cammarata")
row(M, "means–ends diagnosis", "show a method undercuts the aim it was built for",
    "method M, pursued fully, defeats aim A", "a system works against its own purpose",
    "Momentariness would make afflictions ‘unreal’ — undercutting a path built to remove them.", "Waldron p. 78")
row(M, "reflexive turn", "apply your critique to your own method",
    "our own X is also a case of what we criticise", "you’re exempting your own frame",
    "“Mere perception is itself just another perception”; modern historicism is another doxographic rubric.", "Waldron pp. 11, 241")
row(M, "owned reversal", "state a changed view plainly, and why the old one appealed",
    "I used to think X; now Y; X felt right because Z", "correcting yourself or your field",
    "“Convinced much of the field, including me”; “superposition just felt right.”", "Cammarata")
row(M, "homely analogy", "an everyday image whose logic maps the problem exactly",
    "the problem behaves like (everyday thing)", "an abstract dilemma needs a picture",
    "Self-grasping that vanished and returned would be like trick birthday candles that relight.", "Waldron p. 216")
row(M, "vivid extreme case", "test a claim on its most extreme instance",
    "if P, then even (extreme case) — absurd", "the stakes of a view are hidden",
    "Without continuity, “Mother Theresa and Hitler would be in the same state right after they died.”", "Waldron p. 38")
row(M, "evaluative compound", "a precise two-word verdict",
    "adjective + noun that delivers judgement", "closing a point without a paragraph",
    "“Explanatorily vacuous”; “a conceptual cul-de-sac.”", "Waldron pp. 116–117, 315")
row(M, "compressing coda", "end with a few words that carry the whole argument",
    "‘Same ___, better ___.’", "a long argument needs a handle to remember it",
    "“Same neurons, better microscope.”", "Cammarata")
row(M, "arguing wordplay", "a pun that carries the argument, not just decorates it",
    "word A → related word B, where the link is the claim", "only when the sound-link is the logical link",
    "Habits of body, speech and mind give rise to “the habitats we inhabit.”", "Waldron p. 231")

# ---------------- NAMED HEURISTICS AND LAWS ----------------
H = "heuristic"
def h(term, gloss, use, example, source="Lexicon: Named heuristics", notes=""):
    row(H, term, gloss, "", use, example, source, notes)
h("Occam’s razor", "prefer the explanation with the fewest assumptions", "two explanations fit the facts",
  "The style dropped: a conditional trigger explains it without positing a memory leak.")
h("Hickam’s dictum", "a patient can have as many diseases as they please; the counterweight to Occam", "one neat cause is tempting but the facts are many",
  "Fatigue and back pain may be two problems, not one syndrome.", "Lexicon: Clinical rules of thumb")
h("hoofbeats, not zebras", "think of common causes before rare ones", "a rare cause is exciting but unlikely",
  "A headache after a short night: think sleep, not a tumour.", "Lexicon: Clinical rules of thumb")
h("Sutton’s law", "test first for the most likely cause (“go where the money is”)", "choosing what to check first",
  "Cards misaligned? First check the printer is set to flip on the short edge.", "Lexicon: Clinical rules of thumb")
h("Hanlon’s razor", "don’t attribute to malice what stupidity explains", "a slight feels deliberate",
  "Housing answered half your email: assume overload, not dismissal.")
h("Hitchens’s razor", "what is asserted without evidence can be dismissed without evidence", "a claim arrives with no support",
  "“Research shows flashcards don’t transfer” — which study?")
h("Sagan standard", "extraordinary claims require extraordinary evidence", "a claim is far beyond the usual",
  "A viral repo “can reverse-engineer anything”: read its docs before believing it.")
h("Hume’s guillotine", "no “ought” follows from an “is” alone", "a fact is used to settle a duty",
  "“Everyone here is vegetarian” (is) doesn’t give “so you ought to be” (ought).")
h("Brandolini’s law", "refuting nonsense takes far more effort than producing it", "deciding whether to answer a bad claim",
  "One line — “the Heart Sutra is fake” — takes Nattier’s whole paper to answer.")
h("lectio difficilior", "the harder reading is more likely original, because copyists simplify", "two manuscript readings disagree",
  "One witness has an awkward reading, another a smooth one: favour the awkward.")
h("survivorship bias", "judging from only the cases that made it through a filter", "your sample was pre-selected",
  "Judging monastic life only by the monks who stayed.")
h("streetlight effect", "searching where it’s easy to look, not where the answer is", "the convenient source keeps getting used",
  "Searching only what’s online when the reading is in an unscanned manuscript.")
h("the map is not the territory", "a model is not the thing it models (Korzybski)", "a plan or theory is mistaken for the world",
  "The timetable says 7:30 study; the morning says otherwise.")
h("Goodhart’s law", "when a measure becomes a target, it ceases to be a good measure", "you are about to optimise a number",
  "Counting Anki reviews instead of words you can read in a text.", notes="popular wording usually credited to Marilyn Strathern")
h("Campbell’s law", "the more an indicator drives decisions, the more it is corrupted, and the more it distorts what it monitors", "a metric starts deciding outcomes",
  "Rating the dish crew on speed until plates come back greasy.")
h("Conway’s law", "a system mirrors the communication structure of the people who build it", "a design’s seams look like an org chart",
  "A booklet edited by three committees ends up in three styles.")
h("Gall’s law", "a complex system that works grew from a simple one that worked", "planning a big build from scratch",
  "The meditation timer worked as “one bell, one knob” after the many-menu version failed.")
h("Parkinson’s law", "work expands to fill the time available", "a task has no deadline",
  "Given all Saturday for a two-hour task, it takes all Saturday.")
h("Peter principle", "people rise to the level of their incompetence", "promotion rewards the old job, not the new one",
  "The best dishwasher, promoted to supervisor, turns out a middling supervisor.")
h("Pareto principle", "most effects come from a few causes (the 80/20 rule)", "choosing what to fix or learn first",
  "A small share of Pāli words makes up most of what you’ll read.")
h("cobra effect", "a fix that rewards the problem, and so grows it", "an incentive could be gamed",
  "Making whoever leaves dishes stay late — so people stop signing the dish log.")
h("Lindy effect", "the longer a non-perishable thing has lasted, the longer it’s likely to last", "betting on what will endure",
  "A 2,000-year-old sutta will likely outlast this year’s app.")
h("Chesterton’s fence", "don’t remove something until you know why it was put there", "an old rule or rubric looks pointless",
  "Don’t cut a line from the liturgy until you know why it’s there.")
h("satisficing", "taking the first option that’s good enough (Herbert Simon)", "searching for the best costs more than it gains",
  "Buy the first warm Type B tube that fits and is in stock.")
h("sunk cost fallacy", "letting past spending steer the next choice", "“I’ve already put so much into it”",
  "“I’ve done this deck for months, so I should keep it.”")
h("Buridan’s ass", "paralysis between two equally good options", "two choices are close and time is passing",
  "Two equally good winter retreats, and booking neither.")
h("bikeshedding", "effort spent on the trivial part because it’s easy to argue about (Parkinson’s law of triviality)", "a meeting is stuck on details",
  "An hour on the cover font, ten minutes on the translation.")
h("yak shaving", "a chain of side tasks standing between you and the real one", "you’re three steps removed from the goal",
  "To print the cards, rebuild the script, which needs the font, which needs the repo…")
h("Hofstadter’s law", "it always takes longer than you expect, even allowing for Hofstadter’s law", "estimating time",
  "The “two-hour” typesetting job that took the weekend, padding included.")
h("Pyrrhic", "won at a cost that defeats the purpose", "a win would damage what you want",
  "Winning the argument with Housing and losing their goodwill.")
h("Procrustean", "forcing material to fit a scheme", "a framework is bending the facts",
  "Forcing every weak argument into a named fallacy.")
h("second-order effect", "a consequence of a consequence", "a change looks simple",
  "Cheaper rides add traffic that slows every ride.")
h("rubber-duck debugging", "explaining a problem aloud exposes the error", "you’re stuck",
  "Spotting the bug halfway through describing it to Claude.")
h("frequency illusion", "once noticed, a thing seems to appear everywhere", "a new idea seems suddenly common",
  "After learning “enthymeme”, hidden premises seem to be everywhere.")
h("curse of knowledge", "once you know something, you can’t imagine not knowing it", "writing for beginners",
  "A beginners’ Sanskrit handout that skips sandhi as obvious.")
h("Gell-Mann amnesia", "trusting a source on other topics after seeing it get your own field wrong (Michael Crichton)", "a source failed where you could check it",
  "A paper botches Buddhism; you still trust its AI coverage.")
h("Matthew effect", "advantage accrues to those who already have it (Robert Merton)", "success seems self-reinforcing",
  "Much-cited translators get cited more.")
h("Streisand effect", "trying to suppress information spreads it", "deciding whether to hide something",
  "Banning a book in the dorm makes everyone read it.")
h("Overton window", "the range of ideas acceptable in public discussion at a given time", "an idea seems unsayable now",
  "What a community can openly discuss shifts over decades.")

# ---------------- CORRECTIONS from the two independent checks (2026-11-12) ----------------
# C1 = accuracy/attribution check (web-verified where noted in NOTES.md); C2 = card-fit/ambiguity check.
# Kept as overrides so the original draft and every correction stay traceable.
FIX = {
 "genetic fallacy": dict(example="“It was composed in China, so what it says about emptiness is wrong.”", _by="C2: original was misaimed, not empty"),
 "argument from silence": dict(example="“The Nikāyas never mention Amitābha, so the Pure Land teaching is false.”", _by="C2: retarget to truth"),
 "appeal to popularity": dict(example="“Millions chant it, so it must be the Buddha’s own words.”", _by="C2: retarget; old wording cued appeal to tradition"),
 "ignoratio elenchi": dict(gloss="missing the point: an argument, perhaps valid, for a conclusion other than the one at issue", _by="C1: soundness not part of it"),
 "false dilemma": dict(form="A or B (other options ignored); not A; so B", example="“Either I drop Anki or I never finish Gibson.”", _by="C1+C2"),
 "post hoc ergo propter hoc": dict(example="“I wore my mala to the exam and got an A, so the mala works.”", use="only timing links the two", notes="", _by="C2: old example was a legitimate hypothesis (abduction)"),
 "affirming the consequent": dict(example="“Type B tubes flicker on start-up; this one flickers; so it’s Type B.”", _by="C2: duplicated low diagnosticity"),
 "begging the question": dict(example="“Only the Pāli canon is authentic, because only authentic texts made it into the canon.”", _by="C2: match the form"),
 "non sequitur": dict(example="“Gibson’s textbook is beautifully typeset, so its grammar must be right.”", notes="", _by="C2: old example was an enthymeme with a false premise"),
 "fallacy of composition": dict(example="“Each verse is easy, so the whole chapter will be easy.”", _by="C2"),
 "straw man": dict(example="“Madhyamaka says nothing exists — so it’s nihilism, which the Buddha rejected.”", _by="C2: old example was equivocation"),
 "slippery slope": dict(example="“Skip one morning sit, and soon it’s practice, then precepts, then disrobing.”", source="constructed", _by="C2: too close to floodgates"),
 "modus tollens": dict(example="If the printer flipped on the short edge, the backs would line up; they don’t; so it didn’t.", source="constructed", _by="C2: old example was the floodgates case"),
 "disjunctive syllogism": dict(use="always valid; sound only if the two options really exhaust the field (else false dilemma)", example="The file is portrait or landscape; it isn’t portrait; so it’s landscape.", _by="C1: validity vs soundness; C2: old example was itself a false dilemma"),
 "a fortiori": dict(gloss="“all the more so”: if it holds in the harder case, it holds all the more in the easier one", form="if P holds even for X, it holds all the more for Y", _by="C1: direction"),
 "abduction": dict(gloss="inferring a hypothesis that would explain the facts (Peirce); in a stronger sense, inference to the best explanation", _by="C1"),
 "enthymeme": dict(example="“He’s a monk, so he won’t eat after noon.”", form="P; so Q (missing premise: if P then Q)", source="constructed", _by="C2: old example cued floodgates"),
 "principle of charity": dict(gloss="interpret others so their statements come out as true and reasonable as possible; in argument, test the strongest version (steelmanning)",
     notes="Neil Wilson coined it (1959) for fixing what names refer to; Quine and Davidson extended it to translation and interpretation; steelmanning is a later informal-logic extension", _by="C1"),
 "low diagnosticity": dict(example="“He cites Pāli, so he’s Theravāda” — Mahāyāna scholars cite Pāli just as often.", _by="C2: duplicated affirming the consequent; gave the answer away"),
 "peritrope": dict(gloss="turning a thesis back on itself to show it refutes itself (Plato, Theaetetus 171a, against Protagoras)", form="apply “all X are Y” to itself; it comes out not-Y", _by="C1: names the move, not the thesis"),
 "coined handle": dict(source="Waldron pp. 78–84; Cammarata “recursive generalization”", _by="C1: pp."),
 "paired axes": dict(example="The ālaya analysed synchronically (what it supports now) and diachronically (what it carries over time).", _by="C2: old example read as contrastive compression"),
 "rival predictions": dict(example="If composed in Chinese, the Sanskrit should show calques from Chinese; if in Sanskrit, the reverse.", source="constructed (cf. Nattier 1992; Cammarata)", _by="C2: old quote said ‘predict’"),
 "reflexive turn": dict(example="Modern historicism is itself just another doxographic rubric.", _by="C2: other half was a peritrope"),
 "vivid extreme case": dict(form="picture P at its limit: (extreme case)", example="Without continuity, “Mother Theresa [sic] and Hitler would be in the same state right after they died.”", _by="C2: form read as reductio; C1: spelling as printed"),
 "compressing coda": dict(example="The last line of a long essay: “Same neurons, better microscope.”", _by="C2: position cue"),
 "Sutton’s law": dict(example="A bug report? Check yesterday’s edited line before auditing the whole script.", _by="C2: too close to zebras"),
 "Sagan standard": dict(example="A repo “reverse-engineers any firmware”: believe it after independent benchmarks, not its README.", _by="C2"),
 "Hume’s guillotine": dict(example="“Humans evolved to eat meat, so we ought to.”", _by="C2: gave the answer away"),
 "Brandolini’s law": dict(example="One line — “meditation is just relaxation” — takes a whole lecture to unpack.", _by="C1: Nattier is the source of the thesis, not its rebuttal"),
 "Goodhart’s law": dict(example="Aim at 200 Anki reviews a day and you start clicking “Good” on cards you half-know.", _by="C2"),
 "Campbell’s law": dict(example="When housing priority follows GPA, students start avoiding hard seminars.", _by="C2: indicator driving allocation"),
 "Gall’s law": dict(gloss="a complex system that works grew from a simple one that worked; one designed from scratch never works", _by="C1: example shows the second clause"),
 "Hofstadter’s law": dict(example="Budget double for the translation, and it still overruns the doubled budget.", _by="C2: duplicated Parkinson"),
 "Peter principle": dict(example="The best translator, made editor, turns out a middling editor.", _by="C2"),
 "cobra effect": dict(example="Crediting whoever clears the biggest dish backlog — so people let the backlog pile up.", _by="C1+C2: must reward the problem"),
 "sunk cost fallacy": dict(cls="fallacy", _by="C1+C2: a fallacy, not a heuristic"),
 "curse of knowledge": dict(gloss="once you know something, it’s hard to imagine not knowing it", cls="bias", _by="C1"),
 "Gell-Mann amnesia": dict(gloss="trusting a source on other topics after seeing it get your own field wrong (coined by Michael Crichton, 2002, after Murray Gell-Mann)", _by="C1"),
 "survivorship bias": dict(cls="bias", _by="C1: a bias"),
 "frequency illusion": dict(cls="bias", _by="C1: a bias"),
 "streetlight effect": dict(cls="bias", _by="C1: an observational bias"),
 "Pyrrhic": dict(cls="verdict", _by="C1: an evaluative word"),
 "Procrustean": dict(cls="verdict", _by="C1: an evaluative word"),
}
_seen = set()
for r in R:
    f = FIX.get(r["term"])
    if f:
        _seen.add(r["term"])
        for k, v in f.items():
            if k != "_by":
                r[k] = v
        r["checked"] = "C1+C2; corrected (" + f["_by"] + ")"
    else:
        r["checked"] = "C1+C2; no change"
assert _seen == set(FIX), set(FIX) - _seen

# ---------------- PRE-PRINT VERIFICATION (2026-11-14) ----------------
# V1 = every Waldron quote checked against an OCR of Xiu's PDF of Making Sense of Mind Only (pages read from the
#      printed running heads); V2 = independent web check of the named-law / bias rows (URLs in NOTES.md).
FIX2 = {
 "contrastive compression": dict(source="Waldron p. 104", _by="V1: page located"),
 "relocated boundary": dict(example="The private/shared line runs “not … between our skin-encapsulated body and the world, but rather between our material senses and our ‘minds.’”", _by="V1: quote restored to Waldron’s wording"),
 "inline gloss": dict(example="“Each of these dharmas was defined in terms of its own-being (svabhāva).”", _by="V1: quote restored to Waldron’s wording"),
 "paired axes": dict(example="Accounting for an individual “in the present moment—that is, synchronically—” and “over time, diachronically.”", source="Waldron pp. 55, 86", _by="V1: constructed ālaya example replaced by Waldron’s own sentence (p. 86)"),
 "parallel adverbs": dict(source="Waldron p. 160 (his paraphrase of the Saṃdhinirmocana Sūtra)", _by="V1: Waldron marks it as paraphrase"),
 "evaluative compound": dict(source="Waldron p. 116 (explanatorily vacuous); pp. 40, 128, 317 (conceptual cul-de-sac)", _by="V1: pages corrected"),
 "vivid extreme case": dict(_by="V1: ‘Theresa’ confirmed as printed on p. 38"),
 "Hitchens’s razor": dict(example="“Research shows flashcards don’t transfer” — no study named, so it needs no rebuttal.", _by="V2: old example asked for evidence instead of dismissing"),
 "Campbell’s law": dict(gloss="the more a quantitative indicator drives decisions, the more it invites corruption and distorts what it monitors", _by="V2: Campbell says ‘subject to corruption pressures’"),
 "Peter principle": dict(gloss="in a hierarchy, people tend to rise to their level of incompetence", _by="V2: Peter & Hull’s hedge restored"),
 "satisficing": dict(gloss="settling for an option that’s good enough instead of searching for the best (Herbert Simon)", _by="V2: ‘first’ is only one search rule"),
 "Gall’s law": dict(example="A one-page app grew into a working suite; the all-features rewrite never ran.", _by="V2: the timer’s many-menu version was abandoned as painful, not a failed build, so it misstated Gall"),
 "Hanlon’s razor": dict(gloss="don’t attribute to malice what stupidity or plain oversight explains", _by="V2: gloss now covers the example"),
 "Sutton’s law": dict(example="Twenty possible bugs? Run first the one test that rules out most of them.", _by="V2: still read as ‘common cause first’"),
 "Overton window": dict(example="A policy that got you laughed off stage in 1995 is a mainstream panel topic today.", _by="V2: old example restated the gloss"),
 "Brandolini’s law": dict(_by="V2: audit note clarified (the replaced example had cast Nattier as the rebuttal)"),
 "Gell-Mann amnesia": dict(cls="bias", _by="V2: a bias, not a law"),
 "Buridan’s ass": dict(cls="paradox", _by="V2: a paradox, not a law"),
}
_seen2 = set()
for r in R:
    f = FIX2.get(r["term"])
    if f:
        _seen2.add(r["term"])
        for k, v in f.items():
            if k != "_by":
                r[k] = v
        r["checked"] += "; pre-print " + f["_by"]
    elif r["cls"] in ("move", "heuristic", "bias", "verdict", "paradox"):
        r["checked"] += "; pre-print V1/V2 no change"
assert _seen2 == set(FIX2), set(FIX2) - _seen2

if __name__ == "__main__":
    out = sys.argv[1]
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "class", "term", "gloss", "form", "use", "example", "source", "notes", "checked"])
        for i, r in enumerate(R, 1):
            w.writerow([i, r["cls"], r["term"], r["gloss"], r["form"], r["use"], r["example"], r["source"], r["notes"], r["checked"]])
    from collections import Counter
    print(len(R), Counter(r["cls"] for r in R))
