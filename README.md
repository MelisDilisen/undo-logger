# DATABASE SIMULATION – CHECKPOINTING-BASED UNDO LOGGER AND RECOVERER

## SCOPE OF THE PROJECT

This project is a mere simulation of a database management system (DBMS) and specifically its checkpointing based undo logging and recovering system. For this reason, the project does not aim to implement recovery by Redo, or detailed operations done in the main memory. This project mainly focuses on how the undo logging system works, how the transactions inside them affected by the system crash, and how this has repercussions on the non-volatile disk-based logging. For this reason, the project skipped the parts where more complex operations could be implemented on the transactions in the main memory, like adding, or multiplying. In fact, in this project such operations are just summarized as old and new values of the database values, so that the focus will be on the restoring them to their older value, in case of a crash.

## PURPOSE OF THE PROJECT

The purpose of this project is to implement the logging, recovery, and checkpointing algorithms and understand the inner-workings of the server-side of a DBMS. By implementing these algorithms, the project aims to display the error handling by using logging as sort of a dynamic backup system.

The system helps the user manipulate certain database elements and store these changes. After the immediate changes made in the main memory, with certain checkpointing intervals, this information is sent to the log. Eventually, database system stores this information in persistent storage by flushing log, and sends the information to the disk log. After flushing the log, the log in the main memory is auto truncated.

## INTENDED USERS

This project is simulated as an extremely basic online banking database, where the database is expected to perform operations on the DB elements, which in this case, the savings account of the users. During the execution, the users should be ensured of the correct implementations of its transactions, so that, users will trust the database’s success in protecting the integrity of its money.

Below, in the figure 1, is a use-case diagram for the functional requirements of this project.

![Figure 1: Use Case Diagram](/readme_images/usecase.png)

Table 1 is an example table I created about how logging works throughout different types of storages.

![Table 1: Logging](/readme_images/table.png)

### Log Records
Log records used by undo logging approach are shown below;
  1.	START T : Meaning that transaction T started.
  2.	COMMIT T : Meaning that transaction T finished successfully, no further manipulation of DB element is left. The changes done by T can appear on the disk.
  3.	ABORT T : Meaning that transaction could not successfully finish. So, any changes made on the disk should be reverted.
  4.	<T,X,v> : meaning that transaction T made changes on DB element x, whose former value was v. This is an update record form, which occurs with WRITE action. However, these updates are to be seen only on memory not on disk.

Below, in the figure 2, are the input, undo logging output, output of the implementation of the code.

![Figure 2: Inputs and Outputs](/readme_images/outputs.png)
