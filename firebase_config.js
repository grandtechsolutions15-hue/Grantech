// ===== FIREBASE CONFIGURATION =====
const firebaseConfig = {
    apiKey: "AIzaSyDjmZs43YP29UbX6fByixnU0yFJstFaJtw",
    authDomain: "everness-mfi.firebaseapp.com",
    databaseURL: "https://everness-mfi-default-rtdb.firebaseio.com",
    projectId: "everness-mfi",
    storageBucket: "everness-mfi.firebasestorage.app",
    messagingSenderId: "740108285906",
    appId: "1:740108285906:web:c0b9ab47f46a0c55173a0b"
};

// ===== FIREBASE INITIALIZATION =====
let db = null;

function initializeFirebase() {
    try {
        firebase.initializeApp(firebaseConfig);
        db = firebase.database();
        console.log('✅ Firebase initialized successfully');
        return true;
    } catch (error) {
        console.error('❌ Firebase initialization error:', error);
        return false;
    }
}

// ===== DATABASE STRUCTURE =====
/*
Database structure:
/groups/{groupId}
  - id, name, pin, totalSavings, totalLoans, registrationCollected
  - members/
  - transactions/
  - loans/
  - officers/

/transactions/{transactionId}
  - id, date, memberId, memberName, savings, registration, loan
  - status, recordedBy, approvedBy, editedBy, createdAt, approvedAt, editedAt

/loans/{loanId}
  - id, clientName, clientId, amount, purpose, duration, interestRate
  - status, disbursalDate, approvedBy, createdAt

/officers/{officerId}
  - id, name, email, phone, clients, status

/users/{userId}
  - role (group/officer/admin), credentials
*/

// ===== FIREBASE OPERATIONS =====

class FirebaseDB {
    // ===== AUTHENTICATION =====
    static async authenticateUser(userId, role, pin) {
        try {
            const userRef = db.ref(`users/${userId}`);
            const snapshot = await userRef.once('value');
            const userData = snapshot.val();

            if (!userData) {
                console.warn(`User ${userId} not found`);
                return null;
            }

            if (userData.pin !== pin && role === 'group') {
                console.warn('Invalid PIN');
                return null;
            }

            return { id: userId, role, ...userData };
        } catch (error) {
            console.error('Auth error:', error);
            return null;
        }
    }

    // ===== GROUP OPERATIONS =====
    static async getGroup(groupId) {
        try {
            const snapshot = await db.ref(`groups/${groupId}`).once('value');
            return snapshot.val();
        } catch (error) {
            console.error('Error fetching group:', error);
            return null;
        }
    }

    static async updateGroupStats(groupId, stats) {
        try {
            await db.ref(`groups/${groupId}`).update(stats);
            console.log('✅ Group stats updated');
        } catch (error) {
            console.error('Error updating group stats:', error);
        }
    }

    static async getGroupMembers(groupId) {
        try {
            const snapshot = await db.ref(`groups/${groupId}/members`).once('value');
            const members = snapshot.val() || {};
            return Object.values(members);
        } catch (error) {
            console.error('Error fetching members:', error);
            return [];
        }
    }

    // ===== TRANSACTION OPERATIONS =====
    static async recordTransaction(transaction) {
        try {
            const txnRef = db.ref(`transactions/${transaction.id}`);
            await txnRef.set(transaction);
            console.log('✅ Transaction recorded:', transaction.id);
            return transaction.id;
        } catch (error) {
            console.error('Error recording transaction:', error);
            return null;
        }
    }

    static async getTransactions(groupId, status = null) {
        try {
            const snapshot = await db.ref('transactions').once('value');
            let transactions = snapshot.val() || {};
            transactions = Object.values(transactions);

            if (status) {
                transactions = transactions.filter(t => t.status === status);
            }

            // Filter by group if needed
            return transactions.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        } catch (error) {
            console.error('Error fetching transactions:', error);
            return [];
        }
    }

    static async updateTransaction(transactionId, updates) {
        try {
            await db.ref(`transactions/${transactionId}`).update(updates);
            console.log('✅ Transaction updated:', transactionId);
        } catch (error) {
            console.error('Error updating transaction:', error);
        }
    }

    static async approveTransaction(transactionId, approvedBy) {
        try {
            const updates = {
                status: 'approved',
                approvedBy,
                approvedAt: new Date().toISOString()
            };
            await db.ref(`transactions/${transactionId}`).update(updates);
            console.log('✅ Transaction approved:', transactionId);
        } catch (error) {
            console.error('Error approving transaction:', error);
        }
    }

    static async rejectTransaction(transactionId) {
        try {
            await db.ref(`transactions/${transactionId}`).remove();
            console.log('✅ Transaction rejected:', transactionId);
        } catch (error) {
            console.error('Error rejecting transaction:', error);
        }
    }

    // ===== LOAN OPERATIONS =====
    static async createLoan(loan) {
        try {
            const loanRef = db.ref(`loans/${loan.id}`);
            await loanRef.set(loan);
            console.log('✅ Loan created:', loan.id);
            return loan.id;
        } catch (error) {
            console.error('Error creating loan:', error);
            return null;
        }
    }

    static async getLoans(status = null) {
        try {
            const snapshot = await db.ref('loans').once('value');
            let loans = snapshot.val() || {};
            loans = Object.values(loans);

            if (status) {
                loans = loans.filter(l => l.status === status);
            }

            return loans;
        } catch (error) {
            console.error('Error fetching loans:', error);
            return [];
        }
    }

    static async getLoanById(loanId) {
        try {
            const snapshot = await db.ref(`loans/${loanId}`).once('value');
            return snapshot.val();
        } catch (error) {
            console.error('Error fetching loan:', error);
            return null;
        }
    }

    static async updateLoan(loanId, updates) {
        try {
            await db.ref(`loans/${loanId}`).update(updates);
            console.log('✅ Loan updated:', loanId);
        } catch (error) {
            console.error('Error updating loan:', error);
        }
    }

    // ===== OFFICER OPERATIONS =====
    static async getOfficers() {
        try {
            const snapshot = await db.ref('officers').once('value');
            const officers = snapshot.val() || {};
            return Object.values(officers);
        } catch (error) {
            console.error('Error fetching officers:', error);
            return [];
        }
    }

    static async createOfficer(officer) {
        try {
            const officerRef = db.ref(`officers/${officer.id}`);
            await officerRef.set(officer);
            console.log('✅ Officer created:', officer.id);
            return officer.id;
        } catch (error) {
            console.error('Error creating officer:', error);
            return null;
        }
    }

    // ===== MONTHLY REPORTS =====
    static async getMonthlyCollections(month, year) {
        try {
            const snapshot = await db.ref('transactions').once('value');
            let transactions = snapshot.val() || {};
            transactions = Object.values(transactions);

            // Filter by month/year and approved status
            const filtered = transactions.filter(t => {
                const txnDate = new Date(t.date);
                return txnDate.getMonth() === month - 1 &&
                       txnDate.getFullYear() === year &&
                       t.status === 'approved';
            });

            return filtered;
        } catch (error) {
            console.error('Error fetching monthly collections:', error);
            return [];
        }
    }

    // ===== REAL-TIME LISTENERS =====
    static watchTransactions(callback) {
        try {
            db.ref('transactions').on('value', (snapshot) => {
                const transactions = snapshot.val() || {};
                callback(Object.values(transactions));
            });
        } catch (error) {
            console.error('Error setting up transaction listener:', error);
        }
    }

    static watchLoans(callback) {
        try {
            db.ref('loans').on('value', (snapshot) => {
                const loans = snapshot.val() || {};
                callback(Object.values(loans));
            });
        } catch (error) {
            console.error('Error setting up loan listener:', error);
        }
    }

    // ===== BATCH OPERATIONS =====
    static async batchApproveTransactions(transactionIds, approvedBy) {
        try {
            const updates = {};
            transactionIds.forEach(id => {
                updates[`transactions/${id}/status`] = 'approved';
                updates[`transactions/${id}/approvedBy`] = approvedBy;
                updates[`transactions/${id}/approvedAt`] = new Date().toISOString();
            });
            
            await db.ref().update(updates);
            console.log('✅ Batch approved:', transactionIds.length);
        } catch (error) {
            console.error('Error batch approving:', error);
        }
    }

    // ===== STATISTICS =====
    static async getGroupStatistics(groupId) {
        try {
            const transactions = await FirebaseDB.getTransactions(groupId, 'approved');
            const loans = await FirebaseDB.getLoans();

            const stats = {
                totalSavings: transactions.reduce((sum, t) => sum + (t.savings || 0), 0),
                totalRegistration: transactions.reduce((sum, t) => sum + (t.registration || 0), 0),
                totalLoans: loans.reduce((sum, l) => sum + (l.status === 'disbursed' ? l.amount : 0), 0),
                activeLoanCount: loans.filter(l => l.status !== 'closed').length,
                pendingApprovals: (await FirebaseDB.getTransactions(groupId, 'pending')).length
            };

            return stats;
        } catch (error) {
            console.error('Error calculating statistics:', error);
            return null;
        }
    }
}

// Initialize Firebase when script loads
document.addEventListener('DOMContentLoaded', () => {
    initializeFirebase();
});