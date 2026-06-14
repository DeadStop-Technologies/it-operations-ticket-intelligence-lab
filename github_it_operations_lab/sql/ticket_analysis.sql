-- IT Operations Ticket Intelligence Lab
-- Run these queries against data/tickets.db

-- 1. Ticket count by priority
SELECT
    priority,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY priority
ORDER BY priority;

-- 2. SLA success rate
SELECT
    sla_met,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tickets), 2) AS percentage
FROM tickets
GROUP BY sla_met;

-- 3. Average resolution time by priority
SELECT
    priority,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM tickets
GROUP BY priority
ORDER BY priority;

-- 4. Top repeat root causes
SELECT
    root_cause,
    COUNT(*) AS ticket_count
FROM tickets
GROUP BY root_cause
ORDER BY ticket_count DESC
LIMIT 10;

-- 5. Categories with the most escalations
SELECT
    category,
    COUNT(*) AS escalated_tickets
FROM tickets
WHERE escalated = 'Yes'
GROUP BY category
ORDER BY escalated_tickets DESC;

-- 6. Customer segments with the most SLA misses
SELECT
    customer_segment,
    COUNT(*) AS sla_misses
FROM tickets
WHERE sla_met = 'No'
GROUP BY customer_segment
ORDER BY sla_misses DESC;

-- 7. Open tickets by assigned team
SELECT
    assigned_team,
    COUNT(*) AS open_tickets
FROM tickets
WHERE status = 'Open'
GROUP BY assigned_team
ORDER BY open_tickets DESC;
