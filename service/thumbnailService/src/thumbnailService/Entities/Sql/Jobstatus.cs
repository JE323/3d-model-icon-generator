using System;
using System.Collections.Generic;

namespace thumbnailService.Entities.Sql
{
    public partial class Jobstatus
    {
        public Jobstatus()
        {
            Jobs = new HashSet<Jobs>();
        }

        public Guid Id { get; set; }
        public string Name { get; set; }

        public virtual ICollection<Jobs> Jobs { get; set; }
    }
}
