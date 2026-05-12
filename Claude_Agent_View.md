# Claude Agent View - Complete Guide

## Overview

Agent View is a powerful feature in Claude Code that allows you to dispatch and manage multiple AI coding sessions from a single screen. Instead of working on one task at a time, you can run several independent tasks in parallel - fixing bugs, reviewing PRs, investigating logs, and more - all managed from one central dashboard.

## Table of Contents

- [What is Agent View?](#what-is-agent-view)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Monitoring Sessions](#monitoring-sessions)
- [Dispatching New Agents](#dispatching-new-agents)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Session Management](#session-management)
- [Advanced Features](#advanced-features)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)

---

## What is Agent View?

Agent View (`claude agents`) is your command center for background AI sessions. It provides:

- **Visual Dashboard**: See all your sessions at a glance with status indicators
- **Background Processing**: Sessions continue running even when you close your terminal
- **Parallel Execution**: Run multiple independent tasks simultaneously
- **Session Management**: Peek, reply, attach, detach, and organize sessions effortlessly
- **Supervisor Process**: A separate process manages all background sessions independently

### Requirements

- **Version**: Claude Code v2.1.139 or later
- **Status**: Research preview (interface and shortcuts may change)
- **Check version**: `claude --version`

---

## Quick Start

### 1. Open Agent View

```bash
claude agents
```

This opens the agent view dashboard showing all your background sessions.

### 2. Dispatch a Session

Type your prompt in the input at the bottom and press `Enter`. Examples:

```
Fix the flaky test in UserAuthTest
Review and address comments on PR #1234
Investigate why the login service is timing out
Refactor the payment processing module
```

### 3. Monitor Progress

Sessions appear as rows showing:
- Name (auto-generated or custom)
- Current activity
- Time since last change
- Status indicator (working, needs input, completed, etc.)

### 4. Peek and Reply

- Press `Space` on a selected session to see what it's doing
- Type a reply and press `Enter` to respond
- Use `↑` and `↓` to peek at adjacent sessions

### 5. Attach for Full Conversation

- Press `Enter` or `→` to attach and see the full transcript
- Work interactively as if you ran `claude` directly
- Press `←` on an empty prompt to detach and return to agent view

---

## Key Features

### 1. Parallel Task Execution

Run multiple independent tasks simultaneously:
- Fix multiple bugs in parallel
- Review several PRs at once
- Run test suites while debugging other issues
- Refactor different modules concurrently

**Note**: Each session uses your subscription quota independently.

### 2. Peek & Reply

Quick interaction without opening full transcripts:
- Press `Space` to open peek panel
- See what the session needs from you
- View recent output and opened PRs
- Reply directly from the peek panel
- For multiple-choice questions, press number keys to select

### 3. Background Sessions

Sessions run independently without terminal attachment:
- Close your terminal - sessions keep running
- Managed by a supervisor process
- Sessions persist on disk (survive restarts)
- Auto-restart from where they left off

### 4. Smart Organization

**Grouping Options** (toggle with `Ctrl+S`):
- By state (needs input, working, completed)
- By directory

**Organization Features**:
- Pin important sessions (`Ctrl+T`)
- Reorder sessions (`Shift+↑` / `Shift+↓`)
- Collapse groups (press `Enter` on group header)
- Older completed sessions auto-fold into "… N more" row

**Filtering**:
- `a:<name>` - Filter by agent name
- `s:<state>` - Filter by state (e.g., `s:blocked`)
- `#<number>` or PR URL - Find session working on specific PR

### 5. Isolated Worktrees

**Automatic Isolation**:
- Background sessions start in your working directory
- Blocked from writing files initially
- When editing is needed, Claude automatically moves the session into an isolated git worktree under `.claude/worktrees/`
- Each session gets its own worktree - no file conflicts

**Exception Cases** (no worktree created):
- Session already inside a worktree
- Directory isn't a git repository
- Writes outside the working directory

**Cleanup**:
- Worktrees are removed when you delete the session
- Merge or push changes before deleting
- Find worktree path by peeking or attaching to session

---

## Monitoring Sessions

### Session Status Indicators

Each row shows an icon with **two signals**:

**State Indicators** (color/animation):
- **Animated**: Working - Claude is actively running tools or generating responses
- **Yellow**: Needs input - Waiting for your input (permission or answer)
- **Dimmed**: Idle - Waiting for input but not blocked on specific question
- **Green**: Completed - Task finished successfully
- **Red**: Failed - Task ended with an error
- **Grey**: Stopped - Session was stopped manually

**Process Status** (icon shape):
- **✽ / ✻**: Process is running (can reply immediately)
- **∙**: Process exited but restartable (session persisted on disk)
- **✢**: Loop session sleeping between iterations (shows run count and countdown)

### Session Information

Each row displays:
- Session name
- Current activity or status message
- Time since last change
- PR link and CI status (if PR was opened)

**Status Summaries**:
- Generated by your configured Haiku-class model
- Refresh every ~15 seconds while working
- One refresh when each turn ends
- Uses same provider and data usage terms as main session

### Pull Request Integration

When a session opens a PR:
- Row shows PR link
- CI check status indicator
- Failures and PRs always stay visible (don't fold)
- Review and merge directly from the row

---

## Dispatching New Agents

### From Agent View

Type prompt in bottom input and press `Enter`:

```
Fix the bug in UserController line 45
Review PR #789 and suggest improvements
@code-reviewer Check the new authentication flow
@payments-service Add retry logic for failed transactions
```

**Dispatch Modifiers**:
- `<agent-name> <prompt>` - First word matches subagent name
- `@<agent-name>` - Mention subagent anywhere to run it as main agent
- `@<repo>` - Run session in specific repository
- `/<skill>` - Dispatch a packaged skill
- `#<number>` or PR URL - Select existing session working on that PR
- `Shift+Enter` - Dispatch and immediately attach

**Browse Options**:
- Press `Tab` on empty input to browse all subagents
- Press `/` to browse and dispatch skills
- Paste images to include screenshots or diagrams

### From Inside a Session

Background current session while sending instruction:

```
/background
/bg run the test suite and fix any failures
```

The session detaches and continues in background.

### From the Shell

Start background session directly:

```bash
# Basic background session
claude --bg "investigate the flaky SettingsChangeDetector test"

# With specific agent
claude --agent code-reviewer --bg "address review comments on PR 1234"

# With permission mode
claude --permission-mode ask --bg "refactor user authentication"
```

**Output**:
```
backgrounded · 7c5dcf5d
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

### Dispatching to Specific Directory

**Options**:
1. Open `claude agents` in target directory
2. Open in parent directory, mention repo with `@<repo>`
3. From shell: `cd` into directory and run `claude --bg "<prompt>"`
4. When grouped by directory, highlighted row's directory becomes dispatch target

---

## Keyboard Shortcuts

Press `?` in agent view to see all shortcuts.

### Navigation
- `↑` / `↓` - Move between rows
- `→` - Attach to selected session
- `←` - Detach and return to agent view
- `Alt+1` to `Alt+9` - Attach to Nth session in focused group

### Session Interaction
- `Enter` - Attach to session, or dispatch if text in input
- `Shift+Enter` - Dispatch and attach immediately
- `Space` - Open/close peek panel
- `Tab` - Browse all subagents or apply suggestion

### Organization
- `Ctrl+S` - Switch grouping (state ↔ directory)
- `Ctrl+T` - Pin or unpin selected session
- `Ctrl+R` - Rename selected session
- `Shift+↑` / `Shift+↓` - Reorder selected session
- `Enter` on group header - Collapse/expand group

### Management
- `Ctrl+X` - Stop session (press again within 2s to delete)
- `Ctrl+X` on group header - Delete all sessions in group (with confirmation)
- `Ctrl+G` - Open dispatch prompt in $EDITOR

### Exit
- `Esc` - Close peek panel, clear input, or exit
- `Ctrl+C` - Clear input (press twice to exit)
- `Ctrl+Z` - Detach immediately (from attached session)

**Note**: `←` works from any Claude Code session, not just ones attached from agent view.

---

## Session Management

### Shell Commands

Every background session has a short ID for shell management:

```bash
# Open agent view
claude agents

# Attach to session in terminal
claude attach <id>

# Show recent output
claude logs <id>

# Stop a session
claude stop <id>
# or
claude kill <id>

# Restart stopped session
claude respawn <id>

# Restart all stopped sessions
claude respawn --all

# Remove session from list
claude rm <id>
```

### Stopping Sessions

**From Inside Session**:
- `/stop` - End the session
- `←`, `Ctrl+C`, `Ctrl+D`, `Ctrl+Z`, `/exit` - All leave it running

**From Agent View**:
- `Ctrl+X` - Stop session
- `Ctrl+X` again within 2 seconds - Delete permanently

### Session States

**Active States**:
- **Working**: Claude is actively processing
- **Needs input**: Blocked waiting for your response
- **Idle**: Waiting for input but not blocked

**Terminal States**:
- **Completed**: Task finished successfully
- **Failed**: Ended with error
- **Stopped**: Manually stopped

### Detaching Shortcuts

Configure in `/config` to enable/disable the `←` shortcut for backgrounding sessions.

---

## Advanced Features

### Permission Modes

Sessions inherit settings from their execution directory:

**From Agent View**:
- Uses `defaultMode` from settings
- Or `permissionMode` from subagent frontmatter

**From Shell**:
```bash
claude --bg --permission-mode ask "your prompt"
```

**Security Note**: 
- `bypassPermissions` or `auto` mode requires prior interactive acceptance
- Prevents sessions you aren't watching from acting without approval

### Custom Subagents

Define reusable agent configurations with:
- Custom prompts and instructions
- Tool restrictions
- Isolation modes (`isolation: worktree` in frontmatter)
- Permission modes

**Dispatch Subagents**:
- `@subagent-name prompt text`
- `subagent-name prompt text` (first word)
- Press `Tab` to browse available subagents

### Skills

Package recurring workflows as skills:

```bash
# Browse skills
/ (then Tab)

# Dispatch skill
/skill-name
```

### Worktree Management

**Custom Isolation**:
Set `isolation: worktree` in subagent frontmatter to always run in worktree.

**Find Worktree Path**:
- Peek the session
- Or attach and check working directory

**Manual Cleanup** (if needed):
```bash
# List worktrees
git worktree list

# Remove specific worktree
git worktree remove <path>
```

---

## Architecture

### Supervisor Process

**What It Does**:
- Hosts all background sessions
- Separate from your terminal
- Starts automatically on first background session
- Each session is its own Claude Code process, parented to supervisor

**Authentication**:
- Uses same credentials as interactive sessions
- No additional network connections beyond model API

**Process Management**:
- Active/waiting/attached sessions keep running
- Finished unattached sessions stop after ~1 hour (to free resources)
- Transcript and state saved on disk
- Auto-restart on next attach/peek/reply

**Auto-Updates**:
- Supervisor watches installed binary
- Restarts into new version after auto-updater runs
- Background sessions keep running through restart
- Supervisor reconnects to them

### File System Storage

Default location: `~/.claude/`

Custom location: Set `CLAUDE_CONFIG_DIR` environment variable

**Structure**:
```
~/.claude/
├── daemon.log                    # Supervisor log
├── daemon/
│   └── roster.json              # Running sessions list
└── jobs/<id>/
    └── state.json               # Per-session state
```

### Session Lifecycle

1. **Dispatch**: Session starts in working directory
2. **Background**: Runs without terminal attachment
3. **Active**: Keeps process alive while working or waiting
4. **Idle**: After completion, process stops after ~1 hour
5. **Persist**: State saved on disk, restartable anytime
6. **Delete**: Cleanup removes session and worktree

---

## Troubleshooting

### Agent view opens with no sessions

**Cause**: No sessions dispatched yet.

**Solution**: Type a prompt in the input and press `Enter` to dispatch your first session.

### Sessions show as stopped after waking machine

**Cause**: Background sessions don't survive sleep or shutdown.

**Solution**: 
- Attach, peek, or reply to restart individual sessions
- Or run `claude respawn --all` to restart everything

### Session slow to respond after attaching

**Cause**: Process stopped after ~1 hour of idle time (to free resources).

**Solution**: Wait a moment - process is restarting from saved state. Sessions that are working or waiting on you are never stopped this way.

### `.claude/worktrees/` filling up disk space

**Cause**: Worktrees from deleted sessions not cleaned up.

**Solution**:
```bash
# List all worktrees
git worktree list

# Remove specific worktree
git worktree remove <path>
```

See [worktree cleanup documentation](https://code.claude.com/docs/en/worktrees#clean-up-worktrees) for details.

### Sessions not appearing in agent view

**Check**:
- Verify you're in same `CLAUDE_CONFIG_DIR`
- Check supervisor is running
- Review `~/.claude/daemon.log` for errors

### Disable agent view

**Per-user**: Set `disableAgentView: true` in settings

**Environment**: Set `CLAUDE_CODE_DISABLE_AGENT_VIEW=true`

**Organization**: Administrators can set `disableAgentView` in managed settings

---

## Limitations

Agent view is a **research preview** with current limitations:

### Rate Limits
- Background sessions consume subscription usage same as interactive sessions
- Running 10 agents in parallel = ~10x quota usage
- Monitor your usage carefully

### Local Execution
- Sessions run on your machine
- Stop if machine sleeps or shuts down
- Not available in remote/cloud execution yet

### Worktree Cleanup
- Worktrees deleted with the session
- Merge or push changes before deleting session
- Manual cleanup may be needed if deletion fails

### Interface Changes
- Research preview status means shortcuts and UI may change
- Check documentation for your version
- Administrators can disable for organization

### No Mobile/Web UI
- Terminal-only interface currently
- Requires local Claude Code installation

---

## Best Practices

### When to Use Agent View

**Good Use Cases**:
- Multiple independent bugs to fix
- Batch PR reviews
- Parallel test debugging
- Multi-module refactoring
- Long-running investigations

**Not Ideal For**:
- Single complex task requiring constant oversight
- Highly interdependent work
- When you need to be in the conversation constantly

### Workflow Tips

1. **Dispatch Clearly**: Give each session a specific, independent task
2. **Use Peek First**: Check status without full context switch
3. **Pin Important**: Keep high-priority sessions visible
4. **Group by Directory**: When working across multiple projects
5. **Name Descriptively**: Rename sessions (`Ctrl+R`) for clarity
6. **Clean Up Regularly**: Delete completed sessions and merge their work

### Resource Management

1. **Monitor Quota**: Track how many sessions you're running
2. **Stop Unused**: Don't leave sessions idle indefinitely
3. **Batch Similar Tasks**: Dispatch related work together
4. **Use Skills**: Create reusable workflows for recurring tasks

### Collaboration

1. **PR Integration**: Let sessions open PRs for review
2. **CI Visibility**: Monitor PR checks from agent view
3. **Share Results**: Merge session work into main branch
4. **Document Approach**: Use session names to explain what each does

---

## Next Steps

### Related Features

- **[Subagents](https://code.claude.com/docs/en/sub-agents)**: Define reusable agent configurations
- **[Agent Teams](https://code.claude.com/docs/en/agent-teams)**: Coordinate multiple sessions that message each other
- **[Worktrees](https://code.claude.com/docs/en/worktrees)**: Understand git worktree isolation
- **[Run Agents in Parallel](https://code.claude.com/docs/en/agents)**: Compare different parallel execution strategies
- **[Claude Code on Web](https://code.claude.com/docs/en/claude-code-on-the-web)**: Run sessions in managed cloud environment

### Learning Resources

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [Skills Guide](https://code.claude.com/docs/en/skills)
- [Commands Reference](https://code.claude.com/docs/en/commands)
- [Settings Configuration](https://code.claude.com/docs/en/settings)
- [Permissions Guide](https://code.claude.com/docs/en/permissions)

---

## Examples

### Example 1: Bug Fix Sprint

```bash
# Open agent view
claude agents

# Dispatch multiple bug fixes
Fix timeout issue in UserAuth line 142
Fix memory leak in CacheManager
Fix broken validation in PaymentForm
Fix race condition in WebSocketHandler

# Monitor progress with Space
# Reply to questions as needed
# Attach with Enter when you need full context
# Review PRs as sessions complete them
```

### Example 2: Multi-Repo Workflow

```bash
# Open agent view from parent directory containing multiple repos
cd ~/projects
claude agents

# Dispatch to specific repos
@frontend Update button styles to match design system
@backend Add rate limiting to API endpoints  
@mobile Fix crash on Android 12
@docs Document the new authentication flow

# Sessions run in respective repositories
# Each in isolated worktree
# Review and merge independently
```

### Example 3: Code Review Batch

```bash
# Dispatch reviews for multiple PRs
Review PR #123 focusing on security
Review PR #124 focusing on performance
Review PR #125 focusing on test coverage

# Each session reviews independently
# Posts comments or suggestions
# You peek to see findings
# Approve/request changes as needed
```

### Example 4: Test Suite Debugging

```bash
# Start with general task
Run test suite and fix all failures

# Session identifies 5 failing tests
# Dispatch individual fixes
Fix UserTest.testLogin failure
Fix PaymentTest.testRefund failure
Fix AdminTest.testPermissions failure

# Parallel debugging
# Each session focused on one test
# Combine fixes when all complete
```

---

## Conclusion

Agent View transforms Claude Code into a parallel workflow orchestrator. Instead of working on one task at a time, you can:

✅ Dispatch multiple independent tasks  
✅ Monitor all work from one screen  
✅ Intervene only when needed  
✅ Work like a tech lead managing a team  

The research preview status means continuous improvements are coming. Try it out, provide feedback, and explore how parallel AI workflows can boost your productivity.

**Get started today:**
```bash
claude --version  # Check you have v2.1.139+
claude agents     # Open agent view
# Type your first task and press Enter!
```

---

*Last updated: May 2026*
*Based on Claude Code documentation v2.1.139+*  
*Official docs: https://code.claude.com/docs/en/agent-view*
