/* CELPIP Trainer — built-in seed question bank.
   Format-correct CELPIP-General practice content for every task type.
   A larger machine-generated bank (bank.gen.js) is merged on top of this
   at load time when present. Sets window.CELPIP_BANK_SEED. */
window.CELPIP_BANK_SEED = {
  reading: {
    correspondence: [
      {
        id: "seed-corr-1",
        title: "Helping a friend move",
        instructions: "Read the following email, then answer the questions.",
        passage:
`Hi Daniel,

I hope you're settling into your new apartment! I wanted to check in about this weekend. As you know, I finally get the keys to my place on Saturday, and I could really use a hand moving the bigger furniture — especially the couch and that heavy bookshelf.

I've booked a rental van for Saturday morning, so if you're free from around 9 a.m., that would be perfect. I'm hoping we can finish before noon, because the building only lets residents use the service elevator until 1 p.m. on weekends.

If Saturday doesn't work, I could push everything to Sunday, but the van costs more then, so I'd rather not. Let me know either way by Thursday so I can confirm the booking. I'll buy lunch afterward to say thanks!

Talk soon,
Priya`,
        questions: [
          { q: "Why is Priya writing to Daniel?", options: ["To invite him to see her new apartment", "To ask him to help her move furniture", "To return furniture she borrowed", "To recommend a moving company"], answer: 1, explanation: "The email's main request is a hand moving the bigger furniture." },
          { q: "When does Priya get the keys to her new place?", options: ["Thursday", "Friday", "Saturday", "Sunday"], answer: 2, explanation: "She says she 'finally get[s] the keys to my place on Saturday.'" },
          { q: "Why does Priya want to finish before noon?", options: ["The van must be returned by noon", "The service elevator is only available until 1 p.m.", "Daniel is busy in the afternoon", "Lunch is served at noon"], answer: 1, explanation: "The building only allows the service elevator until 1 p.m., so she wants to finish in time." },
          { q: "Why does Priya prefer Saturday over Sunday?", options: ["The van is cheaper on Saturday", "Daniel is only free on Saturday", "The building is closed on Sunday", "She works on Sunday"], answer: 0, explanation: "She notes the van 'costs more' on Sunday, so Saturday is cheaper." },
          { q: "What does the phrase 'use a hand' most nearly mean?", options: ["Borrow money", "Get some help", "Ask for directions", "Take a break"], answer: 1, explanation: "'Use a hand' is an idiom meaning to get help." },
          { q: "By when should Daniel reply?", options: ["Wednesday", "Thursday", "Saturday", "Sunday"], answer: 1, explanation: "She asks him to 'let me know either way by Thursday.'" }
        ]
      }
    ],
    diagram: [
      {
        id: "seed-diag-1",
        title: "Choosing a fitness class",
        instructions: "Read the schedule and the message that follows, then answer the questions.",
        passage:
`RIVERSIDE COMMUNITY CENTRE — Fall Fitness Classes

Class                 | Day       | Time              | Level        | Cost
Yoga Basics           | Monday    | 6:00–7:00 p.m.    | Beginner     | $12
Spin                  | Tuesday   | 7:00–8:00 p.m.    | Intermediate | $15
Aqua Fit              | Wednesday | 10:00–11:00 a.m.  | All levels   | $14
Boxing Fundamentals   | Thursday  | 6:30–7:30 p.m.    | Beginner     | $16
Weekend Bootcamp      | Saturday  | 9:00–10:30 a.m.   | Advanced     | $18

Note: Bring your own mat for Yoga. Drop-ins welcome; members receive $2 off each class.

---

Hi, I'm new to exercising and I work weekdays until 6 p.m., so I can only make classes that start after 6 or on weekends. I'd like something for beginners, and I'm not a member yet. I also can't swim, so anything in the pool is out. Which class would you recommend, and what would it cost me?`,
        questions: [
          { q: "Which class best fits this person?", options: ["Yoga Basics", "Spin", "Boxing Fundamentals", "Weekend Bootcamp"], answer: 2, explanation: "It's for beginners and starts at 6:30 p.m. (after they finish work at 6). Yoga starts at 6:00 (too early), and Weekend Bootcamp is advanced." },
          { q: "How much will this person pay per class?", options: ["$12", "$14", "$16", "$18"], answer: 2, explanation: "Boxing Fundamentals is $16, and they are not a member, so no $2 discount applies." },
          { q: "What must a participant bring for Yoga Basics?", options: ["A mat", "A towel", "Water shoes", "Gloves"], answer: 0, explanation: "The note says 'Bring your own mat for Yoga.'" },
          { q: "Why is Aqua Fit unsuitable for this person?", options: ["It is only for advanced students", "It takes place in the pool and they can't swim", "It is fully booked", "It costs too much"], answer: 1, explanation: "They state they can't swim, so pool classes are out." },
          { q: "When is the only class offered on a weekend?", options: ["Friday", "Saturday", "Sunday", "Monday"], answer: 1, explanation: "Weekend Bootcamp runs on Saturday." }
        ]
      }
    ],
    information: [
      {
        id: "seed-info-1",
        title: "Four volunteer programs",
        instructions: "Read the four paragraphs. For each statement, choose the paragraph that gives the information.",
        passage:
`A) The Green Streets program pairs volunteers with local parks to plant and maintain trees. Volunteers commit to two hours every second weekend from April to October. No experience is needed, and all tools are provided. It is popular with families because children over ten may take part with a guardian.

B) Meals on Wheels relies on drivers to deliver hot lunches to seniors who cannot leave home. Volunteers must have a valid driver's licence and their own vehicle. Shifts run on weekday mornings and take about ninety minutes. Mileage is reimbursed at the end of each month.

C) The Newcomer Language Circle matches fluent English speakers with recent immigrants for weekly conversation practice. Sessions are held online on Tuesday evenings, so volunteers can join from anywhere. A three-hour training workshop is required before starting.

D) The Riverbank Cleanup gathers large groups a few times each year to remove litter from the shoreline. It is a one-time commitment with no ongoing schedule, making it ideal for busy people. Gloves and bags are supplied, and participants receive a certificate of appreciation.`,
        questions: [
          { q: "This program requires volunteers to have their own car.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 1, explanation: "Paragraph B requires a valid driver's licence and their own vehicle." },
          { q: "This program can be done from home.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 2, explanation: "Paragraph C's sessions are online, so volunteers join from anywhere." },
          { q: "This program is a single, one-time commitment.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 3, explanation: "Paragraph D describes a one-time commitment with no ongoing schedule." },
          { q: "This program welcomes children accompanied by an adult.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 0, explanation: "Paragraph A allows children over ten with a guardian." },
          { q: "This program reimburses travel costs.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 1, explanation: "Paragraph B reimburses mileage at the end of each month." },
          { q: "This program requires training before you begin.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 2, explanation: "Paragraph C requires a three-hour training workshop first." },
          { q: "Volunteers in this program receive a certificate.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 3, explanation: "Paragraph D says participants receive a certificate of appreciation." },
          { q: "This program charges volunteers a membership fee.", options: ["Paragraph A", "Paragraph B", "Paragraph C", "Paragraph D", "This information is not given"], answer: 4, explanation: "No paragraph mentions a membership fee, so this information is not given." }
        ]
      }
    ],
    viewpoints: [
      {
        id: "seed-view-1",
        title: "The case for a shorter work week",
        instructions: "Read the article, then answer the questions.",
        passage:
`In recent years, the idea of a four-day work week has moved from the fringes of debate into serious discussion in boardrooms across North America. Supporters argue that compressing the work week improves well-being without sacrificing output. Several trials, including a widely reported study in Iceland, found that workers reported less stress and burnout, while productivity held steady or even rose slightly.

Critics, however, caution that the results may not apply everywhere. Much of the early evidence comes from office-based roles, where tasks can be reorganized or automated. In sectors such as healthcare, retail, and manufacturing, a shorter week may simply mean hiring more staff to cover the same hours, raising costs that could be passed on to customers.

There is also the question of how the extra day is used. Proponents assume it will be spent resting or with family, but some economists note that employees may take on second jobs, which would undermine the health benefits the policy is meant to deliver.

For now, I believe the four-day week is a promising experiment rather than a proven solution. Companies considering it should run their own trials, measure results carefully, and be honest about whether the model truly fits their work. What succeeds in a software firm may fail in a hospital, and pretending otherwise helps no one.`,
        questions: [
          { q: "What is the main idea of the article?", options: ["The four-day week has been proven to work everywhere", "The four-day week is promising but may not suit every industry", "Employers should immediately adopt a four-day week", "Shorter weeks always reduce productivity"], answer: 1, explanation: "The author calls it a 'promising experiment' that may not fit every workplace." },
          { q: "What did the Iceland study reportedly find?", options: ["Productivity fell sharply", "Workers felt less stress while productivity held steady", "Companies lost customers", "Employees worked longer hours"], answer: 1, explanation: "Workers reported less stress and burnout while productivity held steady or rose slightly." },
          { q: "Why might a shorter week be harder in healthcare or retail?", options: ["Those workers dislike time off", "Tasks can't be automated, so more staff may be needed", "They already work four days", "Customers prefer longer hours"], answer: 1, explanation: "In those sectors a shorter week may just mean hiring more staff to cover the same hours." },
          { q: "What concern do some economists raise about the extra day off?", options: ["Employees may take second jobs, undermining the health benefits", "Employees will move away", "Employees will demand more pay", "Employees will retire early"], answer: 0, explanation: "Economists note employees might take on second jobs, undermining the intended health benefits." },
          { q: "What is the author's overall stance?", options: ["Strongly opposed", "Cautiously optimistic — a promising experiment", "Completely certain it works", "Indifferent"], answer: 1, explanation: "The author supports trials but stops short of calling it a proven solution." },
          { q: "The paragraph following this article would most likely discuss:", options: ["How a company can design and measure its own trial", "The history of the eight-hour workday", "Unrelated national tax policy", "How to write a resume"], answer: 0, explanation: "The article ends by urging companies to run and measure their own trials — the natural next topic." }
        ]
      }
    ]
  },

  listening: {
    problemSolving: [
      {
        id: "seed-lps-1",
        title: "A mixed-up order",
        instructions: "Listen to the conversation, then answer the questions.",
        setup: "A customer calls an electronics store about an order.",
        transcript: [
          { speaker: "Customer", line: "Hi, I ordered a wireless keyboard last week, but the box that arrived had a computer mouse inside instead." },
          { speaker: "Agent", line: "Oh, I'm sorry about that. Do you have your order number handy?" },
          { speaker: "Customer", line: "Yes, it's four-four-eight-two-one." },
          { speaker: "Agent", line: "Thanks. I see it here — a black wireless keyboard. It looks like the warehouse mixed up two orders. I can send the correct item today." },
          { speaker: "Customer", line: "That would be great. Do I need to mail the mouse back first?" },
          { speaker: "Agent", line: "No need. Keep it or recycle it — it's not worth the return shipping. I'll email you a label only if you'd prefer to send it." },
          { speaker: "Customer", line: "Okay. When will the keyboard arrive?" },
          { speaker: "Agent", line: "If I ship it now, it should reach you in two business days. I'll also add a ten-percent coupon for the trouble." },
          { speaker: "Customer", line: "Perfect, thank you. Two days works fine." },
          { speaker: "Agent", line: "Great. You'll get a confirmation email within the hour." }
        ],
        questions: [
          { q: "What is the customer's problem?", options: ["The keyboard is broken", "They received the wrong item", "The order never arrived", "They were charged twice"], answer: 1, explanation: "They ordered a keyboard but received a mouse." },
          { q: "What caused the mistake?", options: ["The customer ordered incorrectly", "The warehouse mixed up two orders", "The address was wrong", "The item was out of stock"], answer: 1, explanation: "The agent says the warehouse mixed up two orders." },
          { q: "What does the agent say about the mouse?", options: ["It must be mailed back immediately", "The customer can keep or recycle it", "It will be picked up", "It must be paid for"], answer: 1, explanation: "The agent says keep it or recycle it — a return isn't worth the shipping." },
          { q: "When will the correct item arrive?", options: ["The same day", "In two business days", "In a week", "Next month"], answer: 1, explanation: "The agent says it should arrive in two business days." },
          { q: "What does the agent offer for the inconvenience?", options: ["A full refund", "A ten-percent coupon", "A free membership", "A gift card"], answer: 1, explanation: "The agent adds a ten-percent coupon for the trouble." }
        ]
      }
    ],
    conversation: [
      {
        id: "seed-lc-1",
        title: "Weekend hiking plans",
        instructions: "Listen to the conversation, then answer the questions.",
        setup: "Two friends are making weekend plans.",
        transcript: [
          { speaker: "Maya", line: "Hey Tom, are you still up for the hike on Saturday?" },
          { speaker: "Tom", line: "I want to, but the forecast says rain in the morning. Maybe we should switch to Sunday?" },
          { speaker: "Maya", line: "Sunday's better anyway. The trail gets crowded on Saturdays." },
          { speaker: "Tom", line: "True. Should we do the lakeside loop or the ridge trail?" },
          { speaker: "Maya", line: "The ridge has the best views, but it's steep. If your knee's still bothering you, the lake loop is easier." },
          { speaker: "Tom", line: "My knee's fine now. Let's do the ridge. What time?" },
          { speaker: "Maya", line: "Let's start early, around eight, to beat the heat. I'll bring extra water." },
          { speaker: "Tom", line: "Sounds good. I'll pack some sandwiches. Should we invite Alex?" },
          { speaker: "Maya", line: "Sure, but Alex is slow on hills, so let's warn them it's a tough one." },
          { speaker: "Tom", line: "Ha, fair. I'll text them tonight." }
        ],
        questions: [
          { q: "Why do they change the day?", options: ["The trail is closed Saturday", "Rain is expected Saturday morning", "Tom works Saturday", "Maya is busy"], answer: 1, explanation: "The forecast says rain Saturday morning, so they switch to Sunday." },
          { q: "Which trail do they choose?", options: ["The lakeside loop", "The ridge trail", "A new trail", "They don't decide"], answer: 1, explanation: "Tom says his knee is fine, so they pick the ridge." },
          { q: "Why did they consider the easier trail?", options: ["Tom's knee had been bothering him", "Maya is afraid of heights", "It's shorter", "It's free"], answer: 0, explanation: "Maya suggests the easier loop in case Tom's knee is still bothering him." },
          { q: "What time will they start?", options: ["7 a.m.", "8 a.m.", "9 a.m.", "10 a.m."], answer: 1, explanation: "Maya suggests starting around eight to beat the heat." },
          { q: "What does Maya say about Alex?", options: ["Alex can't come", "Alex is fast", "Alex is slow on hills", "Alex will drive"], answer: 2, explanation: "She notes Alex is slow on hills, so they'll warn them it's tough." }
        ]
      }
    ],
    information: [
      {
        id: "seed-li-1",
        title: "Library orientation",
        instructions: "Listen to the conversation, then answer the questions.",
        setup: "A librarian explains services to a new member.",
        transcript: [
          { speaker: "Member", line: "Hi, I just got my library card. What can I borrow?" },
          { speaker: "Librarian", line: "Welcome! With a standard card you can borrow up to twenty items at once — books, DVDs, and audiobooks." },
          { speaker: "Member", line: "How long can I keep them?" },
          { speaker: "Librarian", line: "Books are three weeks; DVDs are one week. You can renew twice online unless someone else has placed a hold." },
          { speaker: "Member", line: "Is there a fee if I'm late?" },
          { speaker: "Librarian", line: "We went fine-free two years ago, so no late fees. But if an item is more than thirty days overdue, we bill you the replacement cost until it's returned." },
          { speaker: "Member", line: "Good to know. Do you have study rooms?" },
          { speaker: "Librarian", line: "Yes, four of them. They're free, but you must book online, and each booking is limited to two hours a day." },
          { speaker: "Member", line: "Perfect. And printing?" },
          { speaker: "Librarian", line: "Printing is ten cents a page for black and white, and fifty cents for colour. You pay at the front desk." }
        ],
        questions: [
          { q: "How many items can the member borrow at once?", options: ["10", "15", "20", "25"], answer: 2, explanation: "A standard card allows up to twenty items." },
          { q: "How long can books be kept?", options: ["One week", "Two weeks", "Three weeks", "One month"], answer: 2, explanation: "Books are loaned for three weeks (DVDs for one week)." },
          { q: "What happens if an item is over thirty days overdue?", options: ["A daily fine", "The card is cancelled", "They are billed the replacement cost", "Nothing"], answer: 2, explanation: "Items over thirty days overdue are billed at replacement cost until returned." },
          { q: "What is required to use a study room?", options: ["A fee", "An online booking", "A staff escort", "A deposit"], answer: 1, explanation: "Study rooms are free but must be booked online." },
          { q: "How much is colour printing per page?", options: ["10 cents", "25 cents", "50 cents", "It's free"], answer: 2, explanation: "Colour printing is fifty cents per page." },
          { q: "Why are there no late fees?", options: ["The library went fine-free two years ago", "The member is new", "It's a holiday", "Fees are paid yearly"], answer: 0, explanation: "The librarian says they went fine-free two years ago." }
        ]
      }
    ],
    news: [
      {
        id: "seed-ln-1",
        title: "A new pedestrian bridge",
        instructions: "Listen to the news report, then answer the questions.",
        setup: "Listen to a local evening news report.",
        transcript: [
          { speaker: "Reporter", line: "Good evening. The city announced today that the new Riverside pedestrian bridge will open to the public this Saturday, two months ahead of schedule. The bridge connects the east and west banks of the Don River, cutting the walking commute between the two neighbourhoods from twenty-five minutes to under ten." },
          { speaker: "Reporter", line: "Construction began last spring and came in slightly under budget, according to city officials. To celebrate the opening, the city will host a free community festival on Saturday from ten a.m. to four p.m., featuring live music, food trucks, and guided walking tours. Officials are encouraging residents to leave their cars at home, as parking near the site will be limited." }
        ],
        questions: [
          { q: "What is the main story?", options: ["A road closure", "The opening of a new pedestrian bridge", "A music festival cancellation", "A budget cut"], answer: 1, explanation: "The report is about a new pedestrian bridge opening." },
          { q: "When will the bridge open?", options: ["Today", "This Saturday", "Next month", "In spring"], answer: 1, explanation: "It opens this Saturday, two months ahead of schedule." },
          { q: "How does the bridge affect the commute?", options: ["It adds ten minutes", "It cuts it from 25 to under 10 minutes", "It has no effect", "It closes a road"], answer: 1, explanation: "The walking commute drops from twenty-five minutes to under ten." },
          { q: "What is notable about the project's timing and cost?", options: ["Late and over budget", "Ahead of schedule and slightly under budget", "On time and over budget", "Delayed indefinitely"], answer: 1, explanation: "It's two months ahead of schedule and came in slightly under budget." },
          { q: "What are residents encouraged to do?", options: ["Drive to the site", "Leave their cars at home", "Avoid the area", "Pay for parking"], answer: 1, explanation: "Officials encourage leaving cars at home because parking is limited." }
        ]
      }
    ],
    discussion: [
      {
        id: "seed-ld-1",
        title: "Planning a team celebration",
        instructions: "Listen to the discussion, then answer the questions.",
        setup: "Three coworkers plan a team event.",
        transcript: [
          { speaker: "Raj", line: "So, for the team celebration, I was thinking we do a dinner downtown." },
          { speaker: "Lena", line: "Dinner's nice, but it's hard for people with kids to come in the evening. What about a lunch instead?" },
          { speaker: "Raj", line: "That's fair. A weekday lunch could work." },
          { speaker: "Sam", line: "Honestly, some folks are on a tight budget. A fancy restaurant might stress them out. Could we do a potluck in the park?" },
          { speaker: "Lena", line: "I like that — it's free and relaxed. But what if it rains?" },
          { speaker: "Sam", line: "We could book the picnic shelter as a backup. It's covered." },
          { speaker: "Raj", line: "Okay, I'm coming around to the potluck. Lunch, in the park, with the shelter reserved just in case." },
          { speaker: "Lena", line: "Great. I'll make a sign-up sheet so we don't end up with fifteen desserts." },
          { speaker: "Sam", line: "And I'll reserve the shelter for the Saturday after next." },
          { speaker: "Raj", line: "Perfect. Let's send the invite out this week." }
        ],
        questions: [
          { q: "What does Raj originally suggest?", options: ["A park potluck", "A dinner downtown", "A weekend trip", "A movie night"], answer: 1, explanation: "Raj first proposes a dinner downtown." },
          { q: "Why does Lena prefer lunch over dinner?", options: ["It's cheaper", "Evenings are hard for people with kids", "The restaurant closes early", "She works evenings"], answer: 1, explanation: "Lena says evenings are hard for coworkers with children." },
          { q: "What is Sam's concern about a restaurant?", options: ["It's too far", "Some people are on a tight budget", "The food is bad", "It's too small"], answer: 1, explanation: "Sam notes some coworkers are on a tight budget." },
          { q: "What is the backup plan if it rains?", options: ["Cancel the event", "Book the covered picnic shelter", "Move to a restaurant", "Postpone a week"], answer: 1, explanation: "Sam suggests booking the covered picnic shelter." },
          { q: "What will Lena do?", options: ["Reserve the shelter", "Make a sign-up sheet", "Send the invite", "Book a restaurant"], answer: 1, explanation: "Lena offers to make a sign-up sheet." },
          { q: "What do they finally decide?", options: ["A dinner downtown", "A lunchtime potluck in the park", "A catered office lunch", "A weekend hike"], answer: 1, explanation: "They agree on a lunchtime potluck in the park with a shelter backup." }
        ]
      }
    ],
    viewpoints: [
      {
        id: "seed-lv-1",
        title: "Are electric cars really greener?",
        instructions: "Listen to the radio segment, then answer the questions.",
        setup: "Listen to a segment from a radio program.",
        transcript: [
          { speaker: "Host", line: "Welcome back. Today we're talking about electric vehicles, or EVs, and whether they're really the greener choice. Supporters point out that EVs produce no tailpipe emissions, and as more of our electricity comes from wind and solar, driving one gets cleaner every year. That's a strong argument, and it's why many governments are offering rebates to buyers." },
          { speaker: "Host", line: "But it's not the whole picture. Critics note that building an EV battery is energy-intensive and requires mining metals like lithium and cobalt, sometimes under poor labour conditions. So an EV can start its life with a bigger carbon footprint than a gas car, only catching up after tens of thousands of kilometres of driving." },
          { speaker: "Host", line: "My own take? EVs are a genuine step forward, but they're not a magic fix. How clean they are depends heavily on where you live and how the battery was made — and we shouldn't ignore the mining that makes them possible." }
        ],
        questions: [
          { q: "What is the segment mainly about?", options: ["How to buy a car", "Whether EVs are truly greener", "The price of gasoline", "Public transit"], answer: 1, explanation: "The whole segment weighs whether EVs are really the greener choice." },
          { q: "What argument do supporters make?", options: ["EVs are cheaper", "EVs produce no tailpipe emissions and the grid is getting cleaner", "EVs are faster", "EVs need no maintenance"], answer: 1, explanation: "Supporters cite zero tailpipe emissions and a cleaner electricity grid." },
          { q: "What concern do critics raise?", options: ["Battery production is energy-intensive and requires mining", "EVs are too quiet", "EVs can't go far", "EVs are ugly"], answer: 0, explanation: "Critics point to energy-intensive battery production and mining of lithium and cobalt." },
          { q: "When does an EV 'catch up' to a gas car environmentally?", options: ["Immediately", "After tens of thousands of kilometres", "Never", "After one year"], answer: 1, explanation: "The host says it catches up only after tens of thousands of kilometres." },
          { q: "What is the host's own view?", options: ["EVs are a scam", "EVs are a genuine step forward but not a magic fix", "Gas cars are better", "He has no opinion"], answer: 1, explanation: "The host calls EVs a genuine step forward, but not a magic fix." },
          { q: "What does EV cleanliness depend on, according to the host?", options: ["The car's colour", "Where you live and how the battery was made", "The driver's age", "The time of day"], answer: 1, explanation: "He says it depends heavily on your location and how the battery was made." }
        ]
      }
    ]
  },

  writing: {
    email: [
      {
        id: "seed-we-1",
        kind: "email",
        title: "A faulty coffee maker",
        prompt: "You recently bought a coffee maker online, but it stopped working after three days. The company's website asks customers to email support about problems. Write an email to the support team.",
        bullets: ["Explain what you bought and what is wrong with it", "Describe what you have already tried", "Tell them what you would like them to do"],
        timeMin: 27,
        wordRange: "150-200",
        modelAnswer:
`Dear Customer Support,

I am writing about a coffee maker (model BX-200) that I purchased from your website on June 2nd, order number 55127. Although it worked well at first, it stopped turning on after only three days of use.

I have already tried the troubleshooting steps listed in the manual. I checked that the outlet was working by plugging in another appliance, and I made sure the water tank was properly seated. Unfortunately, the machine still does not respond when I press the power button, and no lights come on at all.

Since the product is clearly defective and well within its warranty period, I would like a replacement unit sent to me as soon as possible. If a replacement is not available, I would prefer a full refund instead. I have kept the original packaging and my receipt, and I am happy to return the faulty machine using a prepaid label.

I would appreciate a reply within five business days. Thank you for your help.

Sincerely,
Alex Chen`,
        rubricTips: ["Open by stating the product, order number, and the problem in the first two sentences.", "Use a polite but firm tone — you're reporting a fault, not attacking.", "Give specific evidence of what you tried; it shows you're reasonable.", "State exactly what you want (replacement OR refund) and a deadline.", "Use linking words: although, unfortunately, since, if.", "Aim for 150–200 words and proofread for tense consistency."]
      },
      {
        id: "seed-we-2",
        kind: "email",
        title: "Someone keeps taking your parking spot",
        prompt: "You have lived in your apartment for a year. The parking spot assigned to you is often taken by other people. Write an email to your building manager.",
        bullets: ["Explain the problem and how often it happens", "Describe how it affects you", "Suggest what the manager could do to solve it"],
        timeMin: 27,
        wordRange: "150-200",
        modelAnswer:
`Dear Ms. Thompson,

I am a tenant in unit 304, and I am writing about an ongoing issue with my assigned parking spot, number 12. Over the past month, I have found another vehicle parked in it at least three times a week, usually in the evenings.

When my spot is taken, I have to search the street for parking, which is difficult in winter and sometimes makes me late for my early shifts. On two occasions I had to pay for parking in a nearby lot, even though I already pay for a reserved spot as part of my rent.

I would be grateful if the building could take a few steps to fix this. Clearer signage marking the spots as reserved would help, and a notice reminding residents and their guests not to use assigned spaces might prevent it. If the problem continues, perhaps unauthorized cars could be tagged or towed.

Thank you for looking into this. I look forward to your response.

Best regards,
Jordan Lee`,
        rubricTips: ["Identify yourself (unit number) and the issue immediately.", "Quantify the problem (how often) — it makes your case concrete.", "Explain the real impact on you, not just annoyance.", "Offer two or three reasonable solutions; this reads as cooperative.", "Keep a respectful tone with the manager.", "Close with a polite call to action."]
      }
    ],
    survey: [
      {
        id: "seed-ws-1",
        kind: "survey",
        title: "How to use a vacant downtown lot",
        prompt: "Your city is deciding how to use a vacant downtown lot and has sent residents a survey. Which option do you prefer? Choose one and explain why.",
        bullets: ["Option A: Build a public park with green space and benches", "Option B: Build a parking garage to ease downtown congestion", "Choose ONE option and give reasons to support your choice"],
        timeMin: 26,
        wordRange: "150-200",
        modelAnswer:
`I strongly support Option A: building a public park on the vacant downtown lot.

First, our downtown has very little green space, and residents need somewhere to relax outdoors. A park with trees, benches, and open lawn would give office workers a place to eat lunch and give families a safe spot on weekends. This would make the whole neighbourhood more pleasant and welcoming.

Second, a park offers health and environmental benefits that a parking garage cannot. Green space helps clean the air, provides shade in summer, and encourages people to walk rather than drive. Over time, this could actually reduce traffic instead of simply storing more cars downtown.

I understand that parking is limited, but adding a large garage may only attract more vehicles and worsen congestion in the long run. Improving public transit would be a better way to solve that problem.

For these reasons, I believe a public park is the wiser, healthier choice for our community's future.`,
        rubricTips: ["State your choice clearly in the first sentence.", "Give two or three distinct reasons, each in its own paragraph.", "Support each reason with a concrete example.", "Briefly acknowledge the other option, then explain why yours is better.", "Use linking words: first, second, however, for these reasons.", "Finish with a short, confident conclusion."]
      },
      {
        id: "seed-ws-2",
        kind: "survey",
        title: "Office lunch or work-from-home?",
        prompt: "Your workplace is updating its policy and asked employees to choose between two options in a survey. Which do you prefer? Choose one and explain why.",
        bullets: ["Option A: Work from the office five days a week with a free daily lunch", "Option B: Work from home two days a week with no free lunch", "Choose ONE option and give reasons to support your choice"],
        timeMin: 26,
        wordRange: "150-200",
        modelAnswer:
`I would choose Option B: working from home two days a week, even without a free lunch.

The most important reason is the time and money I would save on commuting. My trip to the office takes over an hour each way, so working from home twice a week would give me back roughly four hours weekly and reduce my transit costs. I could use that time to rest or focus on tasks without interruptions.

In addition, remote days often make me more productive. At home I can concentrate on detailed work without the noise and frequent meetings of the office, and I can adjust my schedule to when I work best.

While a free daily lunch is a nice perk, I do not think a free meal is worth commuting every single day. The flexibility of remote work would improve both my well-being and the quality of my work.

For these reasons, I firmly believe Option B is the better choice for me and many of my colleagues.`,
        rubricTips: ["Pick one option outright — don't sit on the fence.", "Lead with your strongest reason.", "Use personal examples (commute time, focus) to sound genuine.", "Concede the appeal of the other option, then outweigh it.", "Watch verb tenses and keep to 150–200 words.", "End by restating your choice."]
      }
    ]
  },

  speaking: {
    t1: [
      {
        id: "seed-sp1-1", taskNo: 1, type: "Giving Advice", title: "A friend's job offer in another city",
        prompt: "A friend has been offered a job in another city. The pay is better, but they would have to move away from family and friends. They have asked for your advice. What would you tell them?",
        prepSec: 30, speakSec: 90,
        template: ["Open: acknowledge that it's a big decision.", "Advice 1 + reason (e.g., list the pros and cons).", "Advice 2 + reason (e.g., visit the city first).", "A caution (check the cost of living; moving isn't permanent).", "Close: encourage them and offer your support."],
        modelAnswer: "Wow, that's a big decision, so first I'd tell my friend not to rush it. I'd suggest sitting down and making a simple list of the pros and cons — the higher salary and career growth on one side, and being far from family on the other. That usually makes things clearer. Second, I'd advise them to visit the new city before saying yes, maybe for a weekend, to see if they could actually picture themselves living there. I'd also tell them to check the cost of living, because a bigger paycheque doesn't help much if rent is twice as high. And honestly, I'd remind them that moving isn't permanent — if it doesn't work out, they can always come back. Family will still be there, and with video calls, they won't lose touch. In the end, I'd say follow the opportunity if it excites you, but go in with your eyes open. Whatever they choose, I'll support them.",
        tips: ["Give two or three clear pieces of advice, each with a reason.", "Use advice language: 'I'd suggest…', 'If I were you…', 'Make sure to…'.", "Speak for the full time; don't finish in 30 seconds.", "Sound warm and supportive, like talking to a real friend."]
      }
    ],
    t2: [
      {
        id: "seed-sp2-1", taskNo: 2, type: "Talking about a Personal Experience", title: "Learning something difficult",
        prompt: "Describe a time you learned something new that was difficult at first. What was it, and how did you feel once you got better at it?",
        prepSec: 30, speakSec: 60,
        template: ["Set the scene: what, when, where.", "What made it difficult at first.", "What you did to improve.", "How you felt afterward and why it's memorable."],
        modelAnswer: "One thing that was really hard for me at first was learning to skate after I moved to Canada. About two years ago, a friend took me to an outdoor rink downtown in the middle of winter. Honestly, I fell down constantly — my ankles were wobbly and I was holding onto the boards the whole time. It was embarrassing, but I kept going back every weekend and practised pushing off slowly. After about a month, something finally clicked, and I could skate a full lap without falling. I remember feeling so proud and relieved. Now skating is one of my favourite winter activities, and I even go with the same friend every year. Looking back, it taught me that being bad at something at the start is just part of learning.",
        tips: ["Use the past tense throughout and give specific details (when, where, who).", "Tell it like a short story with a beginning, middle, and end.", "Include how you felt — CELPIP rewards natural, personal detail.", "Keep an eye on the clock; 60 seconds goes fast."]
      }
    ],
    t3: [
      {
        id: "seed-sp3-1", taskNo: 3, type: "Describing a Scene", title: "A farmers' market",
        prompt: "Imagine this photo: a busy outdoor farmers' market on a sunny Saturday morning. Wooden stalls are piled with colourful fruit and vegetables. A woman in an apron is handing a paper bag to a customer, while a young boy points at a basket of apples. In the background, a musician plays guitar and people carry cloth shopping bags. Describe this scene to a friend who cannot see it.",
        prepSec: 30, speakSec: 60,
        template: ["General overview (what kind of place, the weather and mood).", "Foreground: the main people and what they're doing.", "Background: what's happening further away.", "Small details: colours, sounds, atmosphere."],
        modelAnswer: "So, this is a photo of a busy outdoor farmers' market, and it looks like a bright, sunny Saturday morning. In the foreground, there are several wooden stalls absolutely piled high with colourful fruits and vegetables — I can see reds, greens, and oranges everywhere. On the right, a woman wearing an apron is handing a brown paper bag to a customer, so she's probably one of the vendors. Just beside her, a little boy is pointing excitedly at a basket of shiny red apples, like he wants his mom to buy some. In the background, there's a musician playing the guitar, which makes the whole place feel relaxed and cheerful. Lots of people are strolling around carrying cloth shopping bags. Overall, it's a lively, friendly scene, and it really feels like a nice community spot.",
        tips: ["Move in order: overview → foreground → background → details.", "Use location phrases: 'in the foreground', 'on the right', 'in the background'.", "Use the present continuous ('is handing', 'are walking').", "Don't just list — add mood words like lively, cheerful, relaxed."]
      }
    ],
    t4: [
      {
        id: "seed-sp4-1", taskNo: 4, type: "Making Predictions", title: "What happens next at the market",
        prompt: "Look at the same farmers' market scene again. The young boy is pointing at a basket of apples while his mother reaches for her wallet. Predict what will probably happen next.",
        prepSec: 30, speakSec: 60,
        template: ["Briefly say what's happening now.", "Prediction 1 (most likely) with 'will' or 'going to'.", "Prediction 2.", "Prediction 3 + a short wrap-up."],
        modelAnswer: "Okay, so right now the little boy is pointing at a basket of apples, and his mother is reaching into her bag for her wallet. Based on that, I think she's probably going to buy some apples for him. The vendor will most likely weigh the apples, put them in a paper bag, and tell the mother the price. Then the mother will pay, probably with cash or a card, and hand the bag to her son, who looks really excited. After that, I'd guess they'll keep walking through the market to check out the other stalls — maybe they'll stop to listen to the musician for a minute. The boy will probably be happily munching on an apple as they go. Overall, it looks like a normal, pleasant shopping trip that's about to end with one very happy kid.",
        tips: ["Start by grounding your prediction in what you see now.", "Use future forms: 'will', 'is going to', 'probably', 'most likely'.", "Give a logical chain of three or more predictions.", "Sound confident even though you're guessing."]
      }
    ],
    t5: [
      {
        id: "seed-sp5-1", taskNo: 5, type: "Comparing and Persuading", title: "Beach resort or big city?",
        prompt: "Your family is choosing a vacation. Option 1: a week at a quiet beach resort with swimming and relaxing. Option 2: a week in a big city with museums, shopping, and nightlife. Choose one and persuade a family member to agree with you.",
        prepSec: 60, speakSec: 60,
        template: ["State your choice clearly.", "Compare on two or three points (cost, activities, rest).", "Address what they might prefer, then counter it.", "Strong closing push."],
        modelAnswer: "Okay, so I really think we should go with the beach resort instead of the big city, and here's why. First, we've all been so busy and stressed this year, and a quiet beach is exactly what we need to actually relax. In the city, we'd be walking all day and probably come home more tired than when we left. Second, the resort is all-inclusive, so once we pay, we don't have to worry about the cost of meals or activities — that makes budgeting way easier. I know you love museums and shopping, and those are fun, but we can do a city trip any long weekend. A proper beach vacation is something we rarely get to do together. Imagine just sitting by the water, swimming, and reading with no schedule at all. Come on — doesn't that sound perfect? Let's book the beach; I promise you'll love it.",
        tips: ["Commit to ONE option and repeat it.", "Compare directly using 'whereas', 'instead of', 'better than'.", "Acknowledge their preference, then outweigh it.", "Use persuasive language: 'imagine…', 'trust me', 'you'll love it'."]
      }
    ],
    t6: [
      {
        id: "seed-sp6-1", taskNo: 6, type: "Dealing with a Difficult Situation", title: "A scheduling conflict",
        prompt: "You promised to help your friend move house on Saturday. But your manager just asked you to work an important shift at the same time, and you really need the extra income. You must call one of them. Decide who to call and what you will say.",
        prepSec: 60, speakSec: 60,
        template: ["State the dilemma briefly.", "Say who you'll call and why.", "What you'll say to them (polite, honest).", "Offer a solution or compromise."],
        modelAnswer: "This is a tricky spot, because I don't want to let my friend down, but I also really need this shift. After thinking about it, I've decided to call my friend, since the shift matters for both my job and my finances. I'd call them and say, 'Hey, I'm so sorry, but something came up at work and I got asked to cover an important shift on Saturday. I feel terrible about the timing.' Then, instead of just cancelling, I'd offer a compromise. I'd say, 'I can still come by Friday evening to help you pack the boxes, and I can ask my brother to help with the heavy lifting on Saturday.' That way my friend still gets support, and I don't lose the shift. I'd also promise to buy them dinner afterward to make up for it. Being honest and offering a backup plan is the best way to handle it without hurting the friendship.",
        tips: ["State your choice and your reason clearly.", "Use polite, apologetic language for the bad news.", "Always offer a compromise or backup — don't just cancel.", "Sound sincere; this task tests tone and diplomacy."]
      }
    ],
    t7: [
      {
        id: "seed-sp7-1", taskNo: 7, type: "Expressing Opinions", title: "Should public transit be free?",
        prompt: "Some people believe that public transportation should be free for everyone. Do you agree or disagree? Explain your opinion with reasons.",
        prepSec: 30, speakSec: 90,
        template: ["State your opinion clearly.", "Reason 1 + example.", "Reason 2 + example.", "Address the other side briefly, then restate."],
        modelAnswer: "In my opinion, public transportation should be free for everyone, and I feel fairly strongly about this. My first reason is environmental. If buses and trains were free, far more people would leave their cars at home, which would cut traffic and reduce air pollution in our cities. For example, in my neighbourhood the roads are jammed every morning, and I'm sure many of those drivers would switch if transit didn't cost them anything. My second reason is fairness. Transportation is a basic need — people have to get to work, school, and medical appointments. For low-income families, even a few dollars a day adds up, and free transit would give everyone equal access to opportunities. Now, I understand the main objection: someone has to pay for it, usually through taxes. That's a fair point, but I'd argue the benefits — cleaner air, less congestion, and a fairer city — are well worth the public investment. So overall, yes, I believe free public transit would make our communities healthier and more equal.",
        tips: ["State your position in the first sentence and stick to it.", "Give two solid reasons, each with an example.", "Acknowledge the opposing view, then rebut it — this shows range.", "You have 90 seconds, so develop your points fully."]
      }
    ],
    t8: [
      {
        id: "seed-sp8-1", taskNo: 8, type: "Describing an Unusual Situation", title: "A dog in a bicycle basket",
        prompt: "Imagine this photo: a small dog is sitting inside the front basket of a bicycle, wearing a tiny yellow raincoat and sunglasses. The bike is parked on a city sidewalk, and a few people nearby are smiling and taking pictures. Describe this unusual scene to a friend over the phone so they can picture it.",
        prepSec: 30, speakSec: 60,
        template: ["Say what's unusual right away.", "Describe the main subject in detail.", "Describe the surroundings and people's reactions.", "End with why it's funny or unusual."],
        modelAnswer: "Okay, you are not going to believe what I'm looking at right now. There's a little dog — I think it's a small white terrier — and it's just sitting calmly inside the front basket of a bicycle. But here's the funny part: the dog is wearing a tiny yellow raincoat, and, I'm not kidding, it also has little sunglasses on. It looks so serious, like it's a tiny commuter heading to work. The bike is parked on a busy city sidewalk, and a few people have stopped to smile and take pictures with their phones. One woman is literally laughing out loud. The weird thing is the dog isn't moving at all — it's totally relaxed, as if this is completely normal for it. Honestly, it's the cutest and strangest thing I've seen all week. You'd love it. I'll try to send you a photo before the owner comes back.",
        tips: ["Lead with what makes the scene unusual.", "Give vivid, specific details (colours, clothing, expressions).", "Describe onlookers' reactions to bring it to life.", "Keep it conversational — you're talking to a friend on the phone."]
      }
    ]
  }
};
