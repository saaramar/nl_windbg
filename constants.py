'''
kd> dt nt!_POOL_DESCRIPTOR
   +0x000 PoolType         : _POOL_TYPE
   +0x008 PagedLock        : _KGUARDED_MUTEX
   +0x008 NonPagedLock     : Uint8B
   +0x040 RunningAllocs    : Int4B
   +0x044 RunningDeAllocs  : Int4B
   +0x048 TotalBigPages    : Int4B
   +0x04c ThreadsProcessingDeferrals : Int4B
   +0x050 TotalBytes       : Uint8B
   +0x080 PoolIndex        : Uint4B
   +0x0c0 TotalPages       : Int4B
   +0x100 PendingFrees     : Ptr64 Ptr64 Void
   +0x108 PendingFreeDepth : Int4B
   +0x140 ListHeads        : [256] _LIST_ENTRY
kd> dt nt!_LIST_ENTRY
   +0x000 Flink            : Ptr64 _LIST_ENTRY
   +0x008 Blink            : Ptr64 _LIST_ENTRY
'''

MY_TAG                  = 0x41414141
GRANULARITY             = 0x10

KERNEL_SHARED_PAGE      = 0xfffff78000000000
USER_SHARED_PAGE        = 0x7ffe0000

NON_PAGED_POOL          = 0
NON_PAGED_NX_POOL       = 0x200

PENDING_OFFSET          = 0x100
FREELIST_OFFSET         = 0x140
PENDING_SIZE            = 0x20

# STATUS return values
STATUS_ERROR            = 0xffffffff
STATUS_SUCCESS          = 0x00000000
STATUS_NOT_IMPLEMENTED  = 0x00000001