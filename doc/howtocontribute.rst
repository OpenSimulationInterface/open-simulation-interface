.. _how-to-contribute:

Contributors' Guidelines
=========================

Introduction
------------

The purpose of this document is to help contributors get started with
the Open Simulation Interface (OSI) codebase.


Reporting issues
----------------

The simplest way to contribute to OSI is to report issues that you may
find with the project on `github <https://github.com/OpenSimulationInterface/open-simulation-interface>`__. Everyone can create issues.
Always make sure to search the existing issues before reporting a new one.
Issues may be created to discuss:

- `Feature requests or Ideas <https://github.com/OpenSimulationInterface/open-simulation-interface/issues/new?assignees=&labels=feature+request&template=feature_request.md&title=>`_
- `Bugs <https://github.com/OpenSimulationInterface/open-simulation-interface/issues/new?assignees=&labels=bug&template=bug_report.md&title=>`_
- `Questions <https://github.com/OpenSimulationInterface/open-simulation-interface/issues/new?assignees=&labels=question&template=question.md&title=>`_
- `Other <https://github.com/OpenSimulationInterface/open-simulation-interface/issues/new>`_

If practicable issues should be closed by a referenced pull request or commit (`here <https://help.github.com/en/articles/closing-issues-using-keywords>`_ you can find keywords to close issues automatically). To help developers and maintainers we provide a `pull request template <https://github.com/OpenSimulationInterface/open-simulation-interface/blob/master/.github/pull_request_template.md>`_ which will be generated each time you create a new pull request.

First steps
-----------

First, make sure that you are proficient enough in protobuf. The developers
website https://developers.google.com/protocol-buffers/ is a great place to start learning.
You may want to make sure that you master these `advanced concepts <https://developers.google.com/protocol-buffers/docs/proto3>`_.

Download and install the protocol buffer on your computer, pick up your favorite programming language and try to encode and decode your custom made osi messages.
It is a good idea to read the `tutorials <https://developers.google.com/protocol-buffers/docs/tutorials>`_ for that in your favorite programming language.

For contribution you also need be proficient in Git. You can download and read the book Pro Git by Scott Chacon and Ben Straub `here <https://link.springer.com/book/10.1007%2F978-1-4842-0076-6>`_ for free.
Learn `how to fork a repository <https://help.github.com/en/articles/fork-a-repo>`_ and follow the suggested `fork workflow <https://www.atlassian.com/git/tutorials/comparing-workflows>`_ by Atlassian.
Become a github guru :).

Where to start
--------------

While you familiarize yourself with the basics as suggested above, you
can have a look at the `doxgen API reference <https://opensimulationinterface.github.io/open-simulation-interface/annotated.html>`_ of OSI. It will
give you an overview of the OSI messages, fields, their main components and their meaning.

Our git workflow
----------------

First, the main repository of the OSI Organization is https://github.com/OpenSimulationInterface/open-simulation-interface.
The other repositories are optional extensions which add functionality to OSI like `validation <https://github.com/OpenSimulationInterface/osi-validation>`_, `visualization <https://github.com/OpenSimulationInterface/osi-visualizer>`_ and `model packaging <https://github.com/OpenSimulationInterface/osi-sensor-model-packaging>`_.
The repository `proto2cpp <https://github.com/OpenSimulationInterface/proto2cpp>`_ is a fork which is used in this organization to convert \*.proto files into \*.cpp files which can be parsed by doxygen to create a `reference documentation <https://opensimulationinterface.github.io/open-simulation-interface/>`_.

Then, there are many ways to use Git, here is ours:

After you have opened an issue, with the tag ``feature request`` or ``idea``
explaining your enhancement to the project, you should
also provide a possible approach or suggest a possible solution.
After a discussion if the feature is plausible or adds value
to the project you can create a pull request
and reference it to your opened issue.

We mostly use squash and merge for pull requests for master.
Instead of seeing all of a
contributor's individual commits from a topic branch,
the commits are combined
into one commit and merged into the master branch.
Once a pull request is ready, it is reviewed and
approved, then squashed using the ``--fast-forward`` option of Git in order to
maintain a streamlined Git history.

**We also enforce a few hygiene rules**:

-  Prefer small atomic commits over a large one that do many things.
-  Don’t mix refactoring and new features.
-  Never mix re indentation, whitespace deletion, or other style changes
   with actual code changes.
-  If you add new osi messages into a \*.proto file, don’t forget to
   extend the documentation and comment on the message and on each field (for more information see :ref:`commenting`).
-  Don't forget to run the unit tests for comment compliance in the folder `tests <https://github.com/OpenSimulationInterface/open-simulation-interface/tree/master/tests>`_ with ``python -m unittest discover tests`` to check if you followed the correct syntax guidelines for \*.proto files
-  Try and mimic the style of commit messages, and for non trivial
   commits, add an extended commit message.

**As per the hygiene of commits themselves**:

-  Give appropriate titles to the commits, and when non-trivial add a
   detailed motivated explanation.
-  Give meaningful and consistent names to branches.
-  Don’t forget to put a ``WIP:`` flag when it is a work in progress


**Our branching workflow summary (member)**:

- Create issues for changes, improvements and ideas!
- Clone repository on your local machine
- Create a branch with a meaningful name: ``prefix/name``, ``feature/new-environmental-conditions``
- prefixes: feature, experimental, bug, etc.
- Add your suggestions to the code Do not use: ``*git add -A *git commit -A``
- The code should compile and pass all `unit tests <https://github.com/OpenSimulationInterface/open-simulation-interface/tree/master/tests>`_ for a pull-request!
- Try to make small changes for easier discussions
- The person willing to merge needs to adjust the version according to :ref:`versioning` before hitting merge


**Our forking workflow summary (no member)**:

- Create a personal fork on your account
- Clone to your local machine
- Make changes
- Create pull-request
- Discuss with issues and with comments in the pull-request
- !!! Consider becoming a member !!!

**Documentation changes**:

- Can be performed by anyone.
- Consider adding stuff to the `osi-documentation <https://github.com/OpenSimulationInterface/osi-documentation>`_ or directly to the `doc <https://github.com/OpenSimulationInterface/open-simulation-interface/tree/master/doc>`_ folder in the repository.
- When new changes are made directly to the osi-documentation repo the documentation will be rebuild and the new changes can be seen. When making documentation changes in the doc folder of the osi repository the changes will be visible when the daily chron job of osi-documentation is executed.

Code Review
-----------

At OSI all the code is peer reviewed before getting committed in the
master branch. Briefly, a code review is a discussion between two or
more developers about changes to the code to address an issue.

Author Perspective
~~~~~~~~~~~~~~~~~~

Code review is a tool among others to enhance the quality of the code and to
reduce the likelihood of introducing new bugs in the code base. It is a
technical discussion, it is not an exam, but it is a common effort to
learn from each other.

These are a few common suggestions we often give while reviewing new code.
Addressing these points beforehand makes the reviewing process easier and less
painful for everybody. The reviewer is your ally, not your enemy.

- Commented code: Did I remove any commented out lines?
  Did I leave a ``TODO`` or an old comment?

- Readability: Is the code easy to understand? Is it worth adding
  a comment to the code to explain a particular operation and its
  repercussion on the rest of the code?

- Variable and function names: These should be meaningful and in line
  with the convention adopted in the code base.

- Are your Commit messages meaningful? (i.e., https://chris.beams.io/posts/git-commit/ )

Review your own code before calling for a peer review from a college.

Reviewer Perspective
~~~~~~~~~~~~~~~~~~~~

Code review can be challenging at times. These are suggestions and common
pitfalls a code reviewer should avoid.

- Ask questions: What is the purpose of this message? If this requirement changes,
  what else would have to change? How could we make this more maintainable?

- Discuss in person for more detailed points: Online comments are useful for
  focused technical questions. In many occasions it is more productive to
  discuss it in person rather than in the comments. Similarly, if discussion
  about a point goes back and forth, It will be often more productive to pick
  it up in person and finish out the discussion.

- Explain reasoning: Sometimes it is best to both ask if there is a better
  alternative and at the same time justify why a problem in the code is worth
  fixing. Sometimes it can feel like the changes suggested are nit-picky
  without context or explanation.

- Make it about the code: It is easy to take notes from code reviews
  personally, especially if we take pride in our work. It is best to make
  discussions about the code than about the developer. It lowers resistance and
  it is not about the developer anyway, it is about improving the quality of
  the code.

- Suggest importance of fixes: While offering many suggestions at once, it is
  important to also clarify that not all of them need to be acted upon and some
  are more important than others. It gives an important guidance to the developer
  to improve their work incrementally.

- Take the developer's opinion into consideration: Imposing a particular design
  choice out of personal preferences and without a real explanation will
  incentivize the developer to be a passive executor instead of a creative agent.

- Do not re-write, remove or re-do all the work: Sometimes it is easier to
  re-do the work yourself discarding the work of the developer. This can give
  the impression that the work of the developer is worthless and adds
  additional work for the reviewer that effectively takes responsibility for
  the code.

- Consider the person you are reviewing: Each developer is a person. If you
  know the person, consider their personality and experience while reviewing their
  code. Sometime it is possible with somebody to be more direct and terse, while
  other people require a more thorough explanation.

- Avoid confrontational and authoritative language: The way we communicate has
  an impact on the receiver. If communicating a problem in the code or a
  suggestion is the goal, making an effort to remove all possible noise from
  the message is important. Consider these two statements to communicate about
  a problem in the code : "This operation is wrong. Please fix it." and
  "Doing this operation might result in an error, can you please
  review it?". The first one implies you made an error (confrontational), and
  you should fix it (authority). The second suggest to review the code because
  there might be a mistake. Despite the message being the same, the recipient might
  have a different reactions to it and impact on the quality of this work. This
  general remark is valid for any comment.

Practicalities : how to ask for a code review.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our code review process uses Github. First a developer creates a new
branch (it is often useful to prefix the name of the branch with the name of
the developer to make it clear at glance who is working on what : e.g.
``john@new-feature``). This is a private new branch, the developer is free to
rebase, squash commits, rewrite history (``git push --force``), etc. at will.

Once the code is ready to be shared with the rest of the team, the developer
opens a Merge Request. It is useful to add a precise description of the code
changes while opening the MR and check if those are in line with the initial
requirements.

If the code is still not ready to be peer reviewed, but it is merely a
RFC, we prefix the MR with ``WIP:`` (work in progress). This will tell everybody
they can look at the code, comment, but there is still work to be done and the
branch can change and history be rewritten.

Finally, when the code is ready to be audited, we remove the WIP status of the
MR and we freeze the branch. From this moment on, the developer will refrain to
rewrite history (but he/she can add new commits) and to rebase the branch
without notice. At this point the developer waits for the reviewer to add his
comments and suggestions.

Github allows to comment both on the code and to add general comments on the
MR. Each comment should be addressed by the developer. He/she can add
additional commits to address each comment. This incremental approach will make
it easier for the reviewer to keep interacting till each discussion is
resolved. When the reviewer is satisfied, he/she will mark the discussion resolved.

When all discussions are resolved, the reviewer will rebase the branch,
squash commits and merge the MR in the master branch.
