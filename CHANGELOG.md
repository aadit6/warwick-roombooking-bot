# Changelog - Warwick Room Booking Bot

## v2.0.0 - Enhanced Testing & Improved Detection

### 🏗️ **Major Changes**

#### **1. Organized Test Structure**
- ✅ Moved all test files to `tests/` directory
- ✅ Created proper Python package structure with `__init__.py`
- ✅ Updated all import paths and documentation

#### **2. Enhanced Bot Logic**
- ✅ **Year-Specific Detection**: Now distinguishes between 2024/25 and 2025/26 systems
- ✅ **Unexpected Change Alerts**: Sends email notifications for unrecognized page changes
- ✅ **Smarter Detection**: More precise logic for "Preferred Start" text matching

#### **3. Comprehensive Test Coverage**
- ✅ **7 Test Scenarios**: Complete coverage of all possible page states
- ✅ **Real Email Testing**: Option to send actual emails during testing
- ✅ **15 Unit Tests**: Full test suite with real environment variables

### 📧 **Email Behavior Changes**

| Page State | Old Behavior | New Behavior |
|------------|-------------|-------------|
| System Unavailable | Print message | Print message ✅ |
| Login Redirect | Send email | Send email ✅ |
| Valid 2025/26 Form | Send email | Send email ✅ |
| **2024/25 Form** | **Send email** | **Send alert email** 🆕 |
| **Unknown Change** | **Print only** | **Send alert email** 🆕 |

### 🧪 **New Test Scenarios**

1. **🔴 System Unavailable** - Current state (prints message)
2. **🟡 Login Redirect** - System live, requires auth (emails notification)
3. **🟡 Return URL** - Alternative login scenario (emails notification)
4. **🟢 Booking Form (2025/26)** - Correct year detected (emails notification)
5. **🟢 Booking Form (Preferred Start)** - Generic form detected (emails notification)
6. **🟠 WRB 2024/25** - Wrong year detected (emails alert) 🆕
7. **🔵 Unknown Change** - Unrecognized page state (emails alert) 🆕

### 🔧 **Technical Improvements**

- ✅ **SSL Email Support**: Fixed port 465 connectivity issues
- ✅ **Modular Testing**: Separated concerns with multiple test files
- ✅ **Import Path Management**: Proper relative imports for test directory
- ✅ **Error Handling**: Enhanced SMTP error detection and reporting

### 📋 **Updated Commands**

#### **Testing Commands:**
```bash
# Unit Tests
uv run python -m unittest tests.test_check_wrb2526 -v

# Scenario Testing
uv run python tests/test_scenarios.py

# Real Email Testing
uv run python tests/test_with_real_email.py

# Page Analysis
uv run python tests/page_summary.py
```

#### **Quick Email Tests:**
```bash
uv run python tests/test_email_simple.py
uv run python tests/test_email.py
```

### ✅ **Verification Results**

- **15/15 Unit Tests Pass**
- **7/7 Scenarios Pass**
- **100% Email Functionality Verified**
- **Real Page Monitoring Working**

### 🎯 **Ready for Production**

The bot now provides:
- **Complete detection coverage** for all possible page states
- **Alert notifications** for unexpected changes
- **Year-specific validation** to avoid false positives
- **Comprehensive testing framework** for ongoing maintenance

**Result: Bot is fully tested and production-ready for Warwick 2025/26 booking detection!** 🚀 